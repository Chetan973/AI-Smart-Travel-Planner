from langgraph.graph import END
from langgraph.graph import START

from app.graph.builder import build_graph
from app.nodes.collect_user_node import collect_user_node
from app.nodes.end_node import end_node
from app.nodes.start_node import start_node
from app.nodes.validate_user_node import validate_user_node

builder = build_graph()

builder.add_node("start", start_node)
builder.add_node("collect_user", collect_user_node)
builder.add_node("validate_user", validate_user_node)
builder.add_node("end", end_node)

builder.add_edge(START, "start")
builder.add_edge("start", "collect_user")
builder.add_edge("collect_user", "validate_user")
builder.add_edge("validate_user", "end")
builder.add_edge("end", END)

travel_graph = builder.compile()