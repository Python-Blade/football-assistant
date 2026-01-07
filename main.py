import streamlit as st
import os
import uuid
from agent import FootballSQLAgent
from pyngrok import ngrok



public_url = ngrok.connect(8501) # put the port provided to you by streamlit
st.write(f"Public URL: {public_url}")



# Page Config
st.set_page_config(page_title="Football Stats Chatbot", layout="wide")

def main():
    st.title("⚽ Football Stats Assistant")
    st.markdown("This bot has access to the data of the Top 5 leagues held from 2014-2020")
    st.divider()
    
    # Initialize session state for agent
    if "agent" not in st.session_state:
        try:
            st.session_state.agent = FootballSQLAgent()
        except Exception as e:
            st.error(f"Failed to initialize agent: {e}")
            return

    # Initialize thread_id
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Enter your query"):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing stats..."):
                try:
                    response_text = st.session_state.agent.ask(prompt, st.session_state.thread_id)
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()