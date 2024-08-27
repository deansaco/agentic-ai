from typing_extensions import TypedDict, List

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    This class defines the structure of the state that is maintained and passed through
    the nodes of our graph-based AI agent. It inherits from TypedDict, which allows
    for type hinting of dictionary keys.

    Attributes:
        question (str): The current question to be processed by the LLM chain. This may
                        be a sub-question derived from the original user query.
        generation (str): The response generated by the LLM based on the current question
                          and available context.
        search (str): A string that acts as a boolean flag ("yes" or "no") indicating
                      whether a web search should be performed for more information.
        documents (List[str]): A list of relevant documents or text snippets used for
                               in-context learning by the LLM.
        steps (List[str]): A record of the steps taken by the agent during its processing,
                           useful for tracking the agent's decision-making process.
        user_query (str): The original question asked by the user. This is stored
                          separately from 'question' to maintain context throughout
                          the processing, especially during the consolidation stage.
        sub_answers (List[str]): A list of answers generated for each sub-question if
                                 the original query was decomposed into multiple parts.
        sub_questions (List[str]): A list of sub-questions generated if the original
                                   query was decomposed into multiple parts.
    """
    question: str
    generation: str
    search: str
    documents: List[str]
    steps: List[str]
    user_query: str
    sub_answers: List[str]
    sub_questions: List[str]
    final_response: str