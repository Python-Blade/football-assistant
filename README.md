# ⚽ Football Data Analyst Chatbot

A powerful AI-powered agent that allows you to query European football data using natural language. Built with LangChain, LangGraph, and Groq's fast Llama 3 models, it converts your questions into SQL queries, executes them against a comprehensive football database, and provides insightful answers.

## 🚀 Features

*   **Natural Language to SQL**: Ask complex questions like "Who won the Premier League in 2016?" or "Which player had the highest xG?" and get accurate answers.
*   **Dual Interface**:
    *   **Streamlit UI**: A user-friendly web interface for interactive chatting.
    *   **FastAPI Backend**: A robust REST API to integrate the agent into other applications.
*   **Public Access**: Built-in **Ngrok** integration to instantly share your local app or API with the world.
*   **Groq Accelerated**: Uses `llama-3.3-70b-versatile` via Groq for lightning-fast inference.

## 🛠️ Tech Stack

*   **Python 3.10+**
*   **Orchestration**: LangChain, LangGraph
*   **LLM**: Groq (Llama 3.3 70B)
*   **Database**: SQLite (SQLAlchemy)
*   **Web**: Streamlit (UI), FastAPI (API)
*   **Tunneling**: Pyngrok

## 📋 Prerequisites

1.  **Groq API Key**: Get one from [console.groq.com](https://console.groq.com).
2.  **HuggingFace Token**: (Optional, if using HF models) from [huggingface.co](https://huggingface.co).
3.  **Ngrok Auth Token**: Get one from [dashboard.ngrok.com](https://dashboard.ngrok.com).

## ⚙️ Installation

1.  **Clone the repository** (or navigate to your project folder).

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    HUGGINGFACE_API_KEY=your_hf_token_here
    NGROK_AUTH_TOKEN=your_ngrok_token_here
    USE_NGROK=true
    ```

4.  **Initialize the Database**:
    This script converts the raw CSV files in `dataset/` into a structured SQLite database (`football.db`).
    ```bash
    python database_setup.py
    ```

## 🖥️ Usage

### 1. Run the Streamlit UI
This launches the interactive chat interface in your browser.
```bash
streamlit run main.py
```
*   **Local URL**: `http://localhost:8501`
*   **Public URL**: Check the terminal output for the Ngrok URL.

### 2. Run the API Server
This starts the FastAPI backend for handling programmatic requests.
```bash
python api.py
```
*   **Local URL**: `http://localhost:8000`
*   **Public URL**: Check terminal output for Ngrok URL.

## 🔌 API Endpoints

The API exposes two main POST endpoints:

| Endpoint | Description | Response Format |
| :--- | :--- | :--- |
| `/query` | Standard endpoint | JSON `{"response": "..."}` |
| `/query-text` | Raw text endpoint | Plain Text String |

### Example Request (cURL)

**JSON Response:**
```bash
curl -X POST "http://localhost:8000/query" ^
     -H "Content-Type: application/json" ^
     -d "{\"query\": \"How many goals did Messi score in 2015?\"}"
```

**Plain Text Response:**
```bash
curl -X POST "http://localhost:8000/query-text" ^
     -H "Content-Type: application/json" ^
     -d "{\"query\": \"Who won the Premier League in 2016?\"}"
```

## 📂 Project Structure

*   `agent.py`: Core logic for the FootballSQLAgent (LangGraph setup).
*   `api.py`: FastAPI server implementation.
*   `main.py`: Streamlit frontend implementation.
*   `database_setup.py`: ETL script to load CSVs into SQLite.
*   `football.db`: The generated SQLite database.
