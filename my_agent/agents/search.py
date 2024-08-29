from my_agent.utils.tools import web_search_tool
from langchain.schema import Document

class WebSearch:
    def __init__(self):
        self.web_search_tool = web_search_tool

    def search(self, state):
        """
        Web search based on the re-phrased question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with appended web results
        """
        print("---Searching the Web---")
        """-----------inputs-----------"""
        documents = state.get("documents", [])
        question = state["question"]
        steps = state["steps"]
        
        """-----------actions-----------"""
        steps.append("web_search")
        web_results = self.web_search_tool.invoke({"query": question})
        documents.extend(
            [
                Document(page_content=d["content"], metadata={"url": d["url"]})
                for d in web_results
            ]
        )
        """-----------outputs-----------"""
        return {
            "documents": documents, 
            "question": question, 
            "steps": steps
        }