import os
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenTextParamsMetaNames
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain.document_loaders.parsers.html import bs4
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
from langchain_chroma import Chroma
#from langchain.vectorstores import Chroma
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader

from langchain_community.embeddings import HuggingFaceBgeEmbeddings

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

index_name = "dean-test"
persist_directory = f"./chroma_db_{index_name}"

# Check if the Chroma database already exists
if os.path.exists(persist_directory):
    # Load existing index from Chroma
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    print(f"Loaded {index_name} from Chroma")
else:
    # List of URLs to load documents from
    urls = [
        "https://en.wikipedia.org/wiki/David_Fincher",
        "https://en.wikipedia.org/wiki/Brad_Pitt"
    ]

    # Load documents from the URLs
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    # Initialize a text splitter with specified chunk size and overlap
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )

    # Split the documents into chunks
    doc_splits = text_splitter.split_documents(docs_list)

    # Create and persist the Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    print(f"Created {index_name} in Chroma")

retriever = vectorstore.as_retriever()
