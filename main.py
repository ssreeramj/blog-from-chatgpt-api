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
from blog_agent import build_graph
from scraper import ChatGPTScraper

load_dotenv()

app = FastAPI(
    title="Blog Generator from ChatGPT",
    version="1.0",
    description="A simple api server that returns back a structured blog from ChatGPT chats.",
)

def format_input(chat_url: str) -> Dict[str, str]:
    scraper = ChatGPTScraper(url=chat_url)
    full_conversation = scraper.get_full_conversation()

    return {
        "blog_title": scraper.title, 
        "full_conversation": full_conversation
    }
    
def format_output(agent_response):
    return agent_response["article"]


blog_writer_agent = build_graph()

add_routes(
    app,
    RunnableLambda(format_input) | blog_writer_agent | RunnableLambda(format_output),
    path="/generate-blog",
)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
