from my_agent.utils.chains import retrieval_grader

class Grader:
    def __init__(self):
        self.retrieval_grader = retrieval_grader

    def grade_documents(self, state):
        """
        Determines whether the retrieved documents are relevant to the question. Store all relevant documents to the documents dictionary. 
        However, if there is even one irrelevant document, then websearch will be invoked.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with only filtered relevant documents
        """
        print("---Grading Retrieved Documents---")
        """-----------inputs-----------"""
        documents = state["documents"]
        question = state["question"]
        steps = state["steps"]
        
        """-----------actions-----------"""
        steps.append("grade_document_retrieval")
        relevant_docs = []
        search = "No"
        
        for d in documents:
            score = self.retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            )
            grade = score["score"]
            if grade == "yes":
                relevant_docs.append(d)
            else:
                search = "Yes"
                continue
        """-----------outputs-----------"""
        return {
            "documents": relevant_docs,
            "question": question,
            "search": search,
            "steps": steps,
        }