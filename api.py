from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from agent import FootballSQLAgent
import uvicorn
import os
from pyngrok import ngrok
from langchain_groq import ChatGroq 


app = FastAPI(title="Football Agent API")



try:
    agent = FootballSQLAgent()
except Exception as e:
    print(f"Failed to initialize agent: {e}")
    agent = None

class QueryRequest(BaseModel):
    query: str
    thread_id: str = "default_thread"

class QueryResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "Football Agent API is running"}




@app.post("/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):

    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized locally.")
    
    try:
        response_text = agent.ask(request.query, request.thread_id)
        return QueryResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query-text", response_class=PlainTextResponse)
def query_agent_text(request: QueryRequest):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized locally.")
    
    try:
        response_text = agent.ask(request.query, request.thread_id)
        return response_text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





if __name__ == "__main__":
       
    try:
        ngrok.kill() 
   
        public_url = ngrok.connect(8000).public_url
        print(f"🚀 Ngrok Tunnel Started: {public_url}")
    except Exception as e:
        print(f"⚠️ Could not start ngrok: {e}")
        print("   (Check your internet connection or DNS settings)")

    uvicorn.run(app, host="0.0.0.0", port=8000)
