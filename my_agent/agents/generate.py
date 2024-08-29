from my_agent.utils.chains import rag_chain

class Generate:
    def __init__(self):
        self.rag_chain = rag_chain

    def generate(self, state):
        """
        Generate answer

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---Generating Response---")
        """-----------inputs-----------"""
        documents = state["documents"]
        question = state["question"]
        steps = state["steps"]

        """-----------actions-----------"""
        steps.append("generating sub-answer")
        generation = self.rag_chain.invoke({"documents": documents, "question": question})
        print("Response to subquestion:", generation)
        
        """-----------outputs-----------"""
        return {
            "documents": documents,
            "question": question,
            "generation": generation,
            "steps": steps,
        }