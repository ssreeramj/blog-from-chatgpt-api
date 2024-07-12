#!/usr/bin/env python
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_groq import ChatGroq
from langserve import add_routes
from typing import Dict
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda
from agent import my_agent

load_dotenv()

app = FastAPI(
    title="Blog Generator from ChatGPT",
    version="1.0",
    description="A simple api server that returns back a structured blog from ChatGPT chats.",
)

def format_input(query: str) -> Dict[str, str]:
    return {
        "messages": [HumanMessage(content=query)]
    }

def format_output(agent_response):
    return agent_response["messages"][-1].content

agent = my_agent()
add_routes(
    app,
    RunnableLambda(format_input) | agent | RunnableLambda(format_output),
    path="/generate-blog",
)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
