import os
import dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq



dotenv.load_dotenv()
hf_token = os.getenv("HUGGINGFACE_API_KEY")

class FootballSQLAgent:


    def __init__(self):

        self.db_path = "sqlite:///football.db"
    
        self.db = SQLDatabase.from_uri(self.db_path)

        
        repo_id = "zai-org/GLM-4.7"

        self.chat_model = ChatGroq(
            temperature=0, 
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.chat_model)
        self.tools = self.toolkit.get_tools()

        self.system_prompt = """ You are a specialized Football Data Analyst Agent interacting with a SQLite database containing European football data.
        The database consists of 7 tables derived from CSV files: appearances, games, leagues, players, shots, teams, and teamstats.

        Your goal is to translate natural language questions about football into syntactically correct SQLite queries, execute them, and provide a clear, insightful answer.

        ### GUIDELINES:
        1. **Initial Exploration:** You MUST start by inspecting the schema of relevant tables using PRAGMA table_info() to understand column names.
        2. **Relational Mapping:** 
            - Use `game_id` to join 'games', 'appearances', 'shots', and 'teamstats'.
            - Use `player_id` to link 'players' to 'appearances' and 'shots'.
            - Use `team_id` to link 'teams' to 'teamstats', 'games', and 'appearances'.
        3. **Query Optimization:** 
            - Limit results to the top 5 unless specified otherwise.
            - Only SELECT specific columns needed.
            - Use ORDER BY for 'top', 'most', 'highest'.
        4. **Safety:** READ-ONLY. No INSERT/UPDATE/DROP.
        5. **Data Context:** 'shots' has xG data. 'teamstats' has possession/shots on target.

        ### EXECUTION FLOW:
        1. Check relevant table schemas.
        2. Construct SQLite query.
        3. Execute query.
        4. Answer the user's question clearly based on the data found.


        GIVE A DETAILED ANSWER. DO NOT GIVE ONE LINER ANSWERS. DO NOT INCLUDE SQL COMMANDS IN THE ANSWER.
        ONLY GIVE RELEVANT DETAILS. DO NOT SAY THINGS LIKE "BASED ON THE QUERY RESULTS", ETC.
        """


        self.agent_executor = create_agent(
            self.chat_model,
            self.tools,
            system_prompt=self.system_prompt,)

    def ask(self, query: str, thread_id: str = "default_thread"):

        """
        Ask the agent a question.
        Returns the final answer string.
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        
        response = self.agent_executor.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config
        )
        
        
        return response["messages"][-1].content
