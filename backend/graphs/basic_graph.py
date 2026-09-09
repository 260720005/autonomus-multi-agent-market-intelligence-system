from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class BasicState(TypedDict):
    message: str

def first_node(state: BasicState):
    return {
        "message": state["message"] + " -> Langgraph is working!"
    }

graph_builder = StateGraph(BasicState)

graph_builder.add_node("first_node", first_node)
graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", END)

graph = graph_builder.compile()


result = graph.invoke({
    "message": "Hello"
})

print(result)