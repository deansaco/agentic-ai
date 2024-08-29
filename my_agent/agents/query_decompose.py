from my_agent.utils.chains import query_decompose_chain

class QueryDecompose:
    def __init__(self):
        self.query_decompose_chain = query_decompose_chain


    def transform_query(self, state: dict) -> dict:
        """
        Transform the user_query to produce a list of simple questions.
        This is the first node invoked in the graph, with input user question and empty steps list
        response = agentic_rag.invoke({"user_query": question3, "steps": []})

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a list of re-phrased question
        """
        """-----------inputs-----------"""
        user_query = state["user_query"]
        steps = state["steps"]
        print("User Query:", user_query)
        print("---Decomposing the QUERY---")
        
        """-----------actions-----------"""
        steps.append("transform_query")
        # Re-write question
        sub_questions = self.query_decompose_chain.invoke({"user_query": user_query})
        
        #parse sub questions as a list
        list_of_questions = [question.strip() for question in sub_questions.strip().split('\n')]
        
        if list_of_questions[0] == 'The question needs no decomposition':
            #no query decomposition required
            #return question field as list
            """-----------outputs-----------"""
            return {
                "sub_questions": [user_query], 
                "steps": steps, 
                "user_query": user_query
            }
        else:
            print("Decomposed into the following queries:", list_of_questions)
            return {
                "sub_questions": list_of_questions, 
                "steps": steps, 
                "user_query": user_query
            }