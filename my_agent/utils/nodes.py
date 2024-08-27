from langchain.schema import Document
from utils.chains import retrieval_grader, rag_chain, query_decompose
from utils.tools import web_search_tool
from utils.vectorstore import retriever
from utils.state import GraphState
from langgraph.graph import START, END, StateGraph
from IPython.display import Image, display


def retrieve(state):
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
    documents = retriever.invoke(question)
    
    """-----------outputs-----------"""
    return {
        "documents": documents, 
        "question": question, 
        "steps": steps
    }
    
def grade_documents(state):
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
        score = retrieval_grader.invoke(
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

def decide_to_generate(state):
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

def web_search(state):
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
    web_results = web_search_tool.invoke({"query": question})
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

def generate(state):
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
    generation = rag_chain.invoke({"documents": documents, "question": question})
    print("Response to subquestion:", generation)
    
    """-----------outputs-----------"""
    return {
        "documents": documents,
        "question": question,
        "generation": generation,
        "steps": steps,
    }
    

#####Outer Loop

def transform_query(state: dict) -> dict:
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
    sub_questions = query_decompose.invoke({"user_query": user_query})
    
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
    
def consolidate(state: dict) -> dict:
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
    final_response = rag_chain.invoke({"documents": qa_pairs, "question": user_query})
    print("Final Response to Original Query:", final_response)
    
    """-----------outputs-----------"""
    return {
        # "user_query": user_query,
        "final_response": final_response
        # "steps": steps,
        # "intermediate_qa": qa_pairs,
    }
    
# intialize Graph
CRAG = StateGraph(GraphState)

# Define the nodes
CRAG.add_node("retrieve", retrieve)  # retrieve
CRAG.add_node("grade_documents", grade_documents)  # grade documents
CRAG.add_node("generate", generate)  # generatae
CRAG.add_node("web_search", web_search)  # web search

# Build graph
CRAG.set_entry_point("retrieve")
CRAG.add_edge("retrieve", "grade_documents")
CRAG.add_conditional_edges(
    "grade_documents",  #at grade_documents node, invoke decide_to_generate function
    decide_to_generate,
    {
        "search": "web_search", #if "search" is returned, invoke the "web_search" node
        "generate": "generate", #if "generate" is returned, invoke the "generate" node
    },
)
CRAG.add_edge("web_search", "generate")
CRAG.add_edge("generate", END)

CRAG_graph = CRAG.compile()

def CRAG_loop(state: dict) -> dict:
    """
    Determines whether to invoke CRAG graph call.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    """-----------inputs-----------"""
    questions = state["sub_questions"] #list of questions
    steps = state["steps"]
    user_query = state["user_query"]   
    
    """-----------actions-----------"""
    sub_answers =[]
    steps.append("entering iterative CRAG for sub questions")
    
    #loop through list of decomposed questions
    for q in questions:
        print("Handling subquestion:", q)
        #enters beggining of CRAG graph -- retrieve node with the following state (question, step)
        response = CRAG_graph.invoke({"question": q, "steps": steps})["generation"]
        sub_answers.append(response)
    
    """-----------outputs-----------"""
    return {
            "sub_answers": sub_answers, 
            "sub_questions": questions, 
            "user_query": user_query
        }