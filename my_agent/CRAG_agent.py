from langgraph.graph import START, END, StateGraph
from my_agent.agents.retriever import Retriever
from my_agent.agents.grader import Grader
from my_agent.agents.generate import Generate
from my_agent.agents.search import WebSearch
from my_agent.agents.router import Router
from my_agent.utils.state import GraphState
from IPython.display import Image, display
from concurrent.futures import ThreadPoolExecutor, as_completed

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CRAG:
    def __init__(self):
        # Initialize agents
        self.retrieve_agent = Retriever()
        self.grade_documents_agent = Grader()
        self.generate_agent = Generate()
        self.web_search_agent = WebSearch()
        self.router_agent = Router()

        # Define the LangGraph Graph
        self.graph = StateGraph(GraphState)

        # Define the nodes
        self.graph.add_node("retrieve", self.retrieve_agent.retrieve)
        self.graph.add_node("grade_documents", self.grade_documents_agent.grade_documents)
        self.graph.add_node("generate", self.generate_agent.generate)
        self.graph.add_node("web_search", self.web_search_agent.search)

        # Build graph
        self.graph.add_edge("retrieve", "grade_documents")
        self.graph.add_conditional_edges(
            "grade_documents",
            self.router_agent.decide_to_generate,
            {
                "search": "web_search",
                "generate": "generate",
            },
        )
        self.graph.add_edge("web_search", "generate")
        self.graph.add_edge("generate", END)

        self.graph.set_entry_point("retrieve")

        self.CRAG_graph = self.graph.compile()
        
    def display_graph(self):
        display(Image(self.CRAG_graph.get_graph(xray=True).draw_mermaid_png()))
        
    def run(self, state: dict) -> dict:
        """
        Determines whether to invoke CRAG graph call.

        Args:
            state (dict): The current graph state

        Returns:
            dict: Updated state with sub_answers, sub_questions, and user_query
        """
        questions = state["sub_questions"]
        steps = state["steps"]
        user_query = state["user_query"]

        sub_answers = []
        steps.append("entering iterative CRAG for sub questions")

        def process_question(q, index):
            print(f"Handling subquestion: {q}")
            return index, self.CRAG_graph.invoke({"question": q, "steps": steps})["generation"]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_question, q, i) for i, q in enumerate(questions)]
            results = [future.result() for future in as_completed(futures)]
        
        # Sort results based on the original order
        sorted_results = sorted(results, key=lambda x: x[0])
        sub_answers = [result[1] for result in sorted_results]

        return {
            "sub_answers": sub_answers,
            "sub_questions": questions,
            "user_query": user_query
        }

# Usage example:
# crag = CRAG()
# result = crag.run(state)