from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()


class LocationInput(BaseModel):
    location: str = Field(..., description="name of the location to get the weather")


# Define the tools for the agent to use
@tool("get-weather")
def search(location: str):
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    if "sf" in location.lower() or "san francisco" in location.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


tools = [search]

tool_node = ToolNode(tools)

# model = ChatGroq(model="llama3-70b-8192").bind_tools(tools)
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)


# Define the function that determines whether to continue or not
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END


# Define the function that calls the model
def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def my_agent():
    # Define a new graph
    workflow = StateGraph(MessagesState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("agent")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        "agent",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge("tools", "agent")

    # Initialize memory to persist state between graph runs
    # checkpointer = MemorySaver()

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable.
    # Note that we're (optionally) passing the memory when compiling the graph
    # agent = workflow.compile(checkpointer=checkpointer)
    agent = workflow.compile()

    return agent


if __name__ == "__main__":
    agent = my_agent()

    final_state = agent.invoke(
        {"messages": [HumanMessage(content="what is the weather in Mumbai?")]},
        config={"configurable": {"thread_id": 42}},
    )

    print(final_state["messages"][-1].content)
