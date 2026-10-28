"""A one-node LangGraph app with no model call, for `droneship run langgraph`."""
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    text: str


def shout(state: State) -> State:
    return {"text": state["text"].upper()}


builder = StateGraph(State)
builder.add_node("shout", shout)
builder.add_edge(START, "shout")
builder.add_edge("shout", END)
graph = builder.compile()
