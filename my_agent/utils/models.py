from langchain_ibm import WatsonxLLM
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenTextParamsMetaNames
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

# Get the OpenAI API key from the .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
