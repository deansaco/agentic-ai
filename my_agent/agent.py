from .agents.query_decompose import QueryDecompose
from .CRAG_agent import CRAG
from .agents.consolidate import Consolidate
from .utils.state import GraphState
from langgraph.graph import START, END, StateGraph
from IPython.display import Image, display

class AgenticRAG:
    def __init__(self):
       # Initialize agents
        self.query_decompose_agent = QueryDecompose()
        self.consolidate_agent = Consolidate()
        self.CRAG_agent = CRAG()

        # Define the LangGraph Graph
        self.master_agent = StateGraph(GraphState)
        
        self.master_agent.add_node("transform_query", self.query_decompose_agent.transform_query)  # retrieve
        self.master_agent.add_node("CRAG_loop", self.CRAG_agent.run)
        self.master_agent.add_node("consolidate", self.consolidate_agent.consolidate)
        
        self.master_agent.set_entry_point("transform_query")
        self.master_agent.add_edge("transform_query", "CRAG_loop")
        self.master_agent.add_edge("CRAG_loop", "consolidate")
        self.master_agent.add_edge("consolidate", END)

        self.agentic_rag = self.master_agent.compile()

    def display_graph(self):
        display(Image(self.agentic_rag.get_graph(xray=True).draw_mermaid_png()))

    def run(self, query, steps=None):
        if steps is None:
            steps = []
        return self.agentic_rag.invoke({"user_query": query, "steps": steps})
    

#test_question = "Is the combined age of Justin Beiber and Bradd Pitt greater than Sidney Crosby's Jersey Number?"

#response = agentic_rag.run({"user_query": test_question, "steps": []})