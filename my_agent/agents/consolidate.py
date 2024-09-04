from my_agent.utils.chains import rag_chain

class Consolidate:
    def __init__(self):
        self.rag_chain = rag_chain

    def consolidate(self, state: dict) -> dict:
        """
        Generate consolidated final answer to the original question, given 1. the original question and 2. the sub_questions with corresponding sub_answers

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---Consolidating Response---")
        """-----------inputs-----------"""
        answers = state['sub_answers']
        questions = state['sub_questions']
        user_query = state['user_query']
        
        """-----------actions-----------"""
        steps = state["steps"]
        steps.append("generating final answer")
        qa_pairs = []
        
        #create a list of the decomposed questions with their corresponding answers
        #this intermediary information is used as context to answer the original user_query via in-context learning / RAG approach
        for i in range(min(len(questions), len(answers))):
            qa_pairs.append({questions[i]: answers[i].strip()})
        print("multi hop context", qa_pairs)
        # final_response = self.rag_chain.stream({"documents": qa_pairs, "question": user_query})
        final_response = self.rag_chain.invoke({"documents": qa_pairs, "question": user_query})
        print("Final Response to Original Query:", final_response)
        
        """-----------outputs-----------"""
        return {
            # "user_query": user_query,
            "final_response": final_response
            # "steps": steps,
            # "intermediate_qa": qa_pairs,
        }