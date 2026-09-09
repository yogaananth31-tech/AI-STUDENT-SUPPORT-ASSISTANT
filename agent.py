import os
import sqlite3
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver

def get_llm():
    # ChatOllama connects to your local hardware; no API key needed
    return ChatOllama(
        model="llama3.1",
        temperature=0.3
    )

@st.cache_resource
def initialize_vector_store():
    docs = []
    data_dir = "./data"
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(data_dir, file))
                docs.extend(loader.load())
    
    if not docs:
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory="./chroma_db")
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def get_agent_executor(thread_id: str = "default_thread"):
    retriever = initialize_vector_store()
    llm = get_llm()
    
    tools = []
    if retriever:
        retriever_tool = Tool(
            name="university_document_search",
            func=lambda q: "\n".join([d.page_content for d in retriever.invoke(q)]),
            description="Searches university regulations, syllabi, FAQs, and notices for accurate answers."
        )
        tools.append(retriever_tool)

    conn = sqlite3.connect("chat_history.db", check_same_thread=False)
    memory = SqliteSaver(conn)

    agent_executor = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory
    )
    
    return agent_executor

def create_agent(thread_id: str = "default_thread"):
    return get_agent_executor(thread_id)
