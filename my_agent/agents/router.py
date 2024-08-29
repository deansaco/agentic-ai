class Router:
    def __init__(self):
        pass

    def decide_to_generate(self, state):
        """
        Determines whether to generate an answer, or re-generate a question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """
        print("---At decision Edge---")
        """-----------inputs-----------"""
        search = state["search"]
        
        """-----------actions & outputs-----------"""
        if search == "Yes":
            return "search"
        else:
            return "generate"