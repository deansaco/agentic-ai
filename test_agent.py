#import pytest
from my_agent.agent import AgenticRAG

def test_agentic_rag_invoke():

    rag = AgenticRAG()
    
    #Test query
    test_query = "What is the capital of France and England and the population of France and England?"
    
    # Invoke the RAG
    response = rag.run(test_query)
    
    # print(response)

    # # Assert that the response is not empty
    # assert response, "Response should not be empty"
    
    # # Assert that the response contains a final_response key
    # assert 'final_response' in response, "Response should contain a 'final_response' key"
    
    # # Assert that the final_response is a non-empty string
    # assert isinstance(response['final_response'], str) and response['final_response'].strip(), "final_response should be a non-empty string"
    
    # # Print the final response
    # print("Final Response:", response['final_response'])

if __name__ == "__main__":
    test_agentic_rag_invoke()
