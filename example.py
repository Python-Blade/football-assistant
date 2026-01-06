from langchain_community.utilities import SQLDatabase
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent





load_dotenv()
hf_token = os.getenv("HUGGINGFACE_API_KEY")

def main():

    st.title("Football Assistant")
    st.markdown("This bot has access to the data of the Top 5 leagues held from 2014-2020")
    st.divider()

    repo_id = "zai-org/GLM-4.7"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id, 
        temperature=0.5, 
        huggingfacehub_api_token=hf_token,
        max_new_tokens=1024,
        stop_sequences=["<|endoftext|>", "</s>", "[/ASSIST]"]
    )

    model = ChatHuggingFace(llm=llm)

    db = SQLDatabase.from_uri("sqlite:///football.db")

    toolkit = SQLDatabaseToolkit(db=db, llm=model)

    tools = toolkit.get_tools()


    prompt = """
        You are a specialized Football Data Analyst Agent interacting with a SQLite database containing European football data.
        The database consists of 7 tables derived from CSV files: appearances, games, leagues, players, shots, teams, and teamstats.

        Your goal is to translate natural language questions about football into syntactically correct SQLite queries, execute them, and provide a clear, insightful answer.

        ### GUIDELINES:
        1. **Initial Exploration:** You MUST start by inspecting the schema of relevant tables using PRAGMA table_info() to understand column names (e.g., checking if goals are in 'appearances' or 'shots').
        2. **Relational Mapping:** - Use `game_id` to join 'games', 'appearances', 'shots', and 'teamstats'.
            - Use `player_id` to link 'players' to 'appearances' and 'shots'.
            - Use `team_id` to link 'teams' to 'teamstats', 'games', and 'appearances'.
        3. **Query Optimization:** - Unless specified otherwise, limit results to the top {top_k}.
            - Only SELECT the specific columns needed to answer the question.
            - Use ORDER BY when looking for 'top scorers', 'most appearances', or 'highest xG'.
        4. **Safety & Constraints:**
            - Strictly READ-ONLY. No INSERT, UPDATE, DELETE, or DROP statements.
            - If a query fails, analyze the error, rewrite the logic, and retry.
        5. **Data Context:** - When asked about 'performance', consider columns in 'teamstats' (like possession, shots on target) or 'appearances'.
            - 'shots.csv' likely contains xG (Expected Goals) data; use it for advanced efficiency questions.

        ### EXECUTION FLOW:
        1. List tables to confirm availability.
        2. Query the schema of the most relevant tables for the specific question.
        3. Construct and double-check the SQL query for {dialect} compatibility.
        4. Execute and summarize the findings in a conversational but data-driven tone.

        """.format(
            dialect="SQLite",
            top_k=5,
        )

    agent = create_agent(
        model,
        tools,
        system_prompt=prompt,)

    input = st.chat_input("Enter your query")
    
    
    if input:
        with st.chat_message("user"):
            st.markdown(input)
        st.divider()

        result = agent.invoke({"messages": [{"role": "user", "content": str(input)}]})

        with st.chat_message("assistant"):
            st.markdown(result["messages"][-1].content)


    

if __name__ == "__main__":
    main()

