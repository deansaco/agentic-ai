from my_agent.utils.vectorstore import retriever

class Retriever:
    def __init__(self):
        self.retriever = retriever

    def retrieve(self, state):
        """
        Retrieve documents
        This is the first Node invoked in the CRAG_graph
        
        # CRAG_graph is invoked in the CRAG_loop node:
        #response = CRAG_graph.invoke({"question": q, "steps": steps})["generation"]
        #we initialize the state with a sub-question and list of steps

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---Retrieving Documents---")
        """-----------inputs-----------"""
        question = state["question"]
        steps = state["steps"]
        
        """-----------actions-----------"""
        steps.append("retrieve_documents")
        documents = self.retriever.invoke(question)
        
        """-----------outputs-----------"""
        return {
            "documents": documents, 
            "question": question, 
            "steps": steps
        }