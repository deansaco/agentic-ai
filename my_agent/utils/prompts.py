from langchain.prompts import PromptTemplate

rag_prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are an assistant for question-answering tasks. 
    {{Below is some context from different sources followed by a user's question. Please answer the question based on the context.
    
    Documents: {documents}}} <|eot_id|><|start_header_id|>user<|end_header_id|>
    
    {{ Question: {question} }}<|eot_id|><|start_header_id|>assistant<|end_header_id|> 
    
    Answer:
    """,
    input_variables=["question", "documents"],
)

grader_prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a grader assessing relevance of a retrieved document to a user question. \n 
    Here is the retrieved document: \n\n {document} \n\n
    
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Here is the user question: {question} \n
    
    Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question. \n
    Provide the binary score as a JSON with a single key 'score' and no preamble or explanation. <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "document"],
)

query_decomposition_prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an assistant for question-answering tasks. 
    Perform query decomposition. Given a user question, break it down into distinct sub questions that \
    you need to answer in order to answer the original question. Response with \"The question needs no decomposition\" when no decomposition is needed.
    Generate questions that explicitly mention the subject by name, avoiding pronouns like 'these,' 'they,' 'he,' 'she,' 'it,' etc. Each question should clearly state the subject to ensure no ambiguity. 
    
    Example 1:
    Question: Is Hamlet more common on IMDB than Comedy of Errors?
    Decompositions: 
    How many listings of Hamlet are there on IMDB?
    How many listing of Comedy of Errors is there on IMDB?
    
    Example 2:
    Question: What is the Capital city of Japan?
    Decompositions:
    The question needs no decomposition
    
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Question: {user_query} <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    Decompositions:"
    """,
    input_variables=["user_query"],
)