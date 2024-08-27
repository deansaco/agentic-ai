from utils.nodes import retrieve, grade_documents, generate, web_search, decide_to_generate, transform_query, consolidate
from utils.state import GraphState
from langgraph.graph import START, END, StateGraph
from IPython.display import Image, display

# intialize Graph
CRAG = StateGraph(GraphState)

# Define the nodes
CRAG.add_node("retrieve", retrieve)  # retrieve
CRAG.add_node("grade_documents", grade_documents)  # grade documents
CRAG.add_node("generate", generate)  # generatae
CRAG.add_node("web_search", web_search)  # web search

# Build graph
CRAG.set_entry_point("retrieve")
CRAG.add_edge("retrieve", "grade_documents")
CRAG.add_conditional_edges(
    "grade_documents",  #at grade_documents node, invoke decide_to_generate function
    decide_to_generate,
    {
        "search": "web_search", #if "search" is returned, invoke the "web_search" node
        "generate": "generate", #if "generate" is returned, invoke the "generate" node
    },
)
CRAG.add_edge("web_search", "generate")
CRAG.add_edge("generate", END)

CRAG_graph = CRAG.compile()

display(Image(CRAG_graph.get_graph(xray=True).draw_mermaid_png()))