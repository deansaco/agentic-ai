from my_agent.utils.prompts import rag_prompt, grader_prompt, query_decomposition_prompt
from my_agent.utils.models import llm
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

#define rag chain
rag_chain = rag_prompt | llm | StrOutputParser()

#define retieval grader chain
retrieval_grader = grader_prompt | llm | JsonOutputParser()

#define query decomposition chain
query_decompose_chain = query_decomposition_prompt | llm| StrOutputParser()