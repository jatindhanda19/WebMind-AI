#IMPORTS Required libraries
import os
import streamlit as st
from dotenv import load_dotenv

#Langchain message types for chat
from langchain_core.messages import AIMessage, HumanMessage

#Load website content
from langchain_community.document_loaders import WebBaseLoader

#Split long text into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

#vector database
from langchain_community.vectorstores import FAISS
#LLM via Groq API
from langchain_groq import ChatGroq

#prompt templates
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Chains for conversational retrieval
from langchain.chains import create_history_aware_retriever , create_retrieval_chain

#combines retrieved documents 
from langchain.chains.combine_documents import create_stuff_documents_chain

#Embedding models
from langchain_community.embeddings import HuggingFaceEmbeddings

#Load Environment Variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


#Streamlit Page Config
st.set_page_config(page_title="Chat with website",
                    page_icon="🤖", layout="wide")
   
#Create Vectorstore from website
def get_vectorstore_from_url(url:str):
    """
    Load website content, splits it into chunks,and 
    create a FAISS vector store using  embeddings.
    """
    #Load website content
    loader = WebBaseLoader(web_path=url,
    bs_kwargs=dict(
        parse_only=None
    ))
    documents = loader.load()

    #Split the text into overlapping chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)

    chunks = splitter.split_documents(documents)

    # create embeddings using MiniLM model
    embeddings = HuggingFaceEmbeddings(
        model_name = "all-MiniLM-L6-v2"
    )
    # Build FAISS vector database
    return FAISS.from_documents(chunks ,embeddings)

#Build Context-Aware Retriever
@st.cache_resource(show_spinner=False)
def build_retriever_chain(vector_store):
    """
    Creates a retriever that is uses of chat history to generate better search queries for relevant document chunks.
    """
    llm = ChatGroq(model="llama3-8b-8192", temperature=0)

    #Retrieve top-k relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    #Prompt to convert conversation search query
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation,generate a search query to look up in order")
    ])
    return create_history_aware_retriever(llm, retriever, prompt)   

#Build conversational RAG Chain
def build_rag_chain(retriever_chain):
    """
    Combines document retrieval with an LLM to generate context
    grounded answers
    """
    llm = ChatGroq(model="llama3-8b-8192",temperature=0.2)

    #System prompt enforcing grounded response
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are a helpful AI assistant.\n"
     "Answer ONLY using the provided context.\n"
     "If the answer is not present in the context, say:\n"
     "'The website does not contain this information.'\n\n"
     "Context:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
    ])
    # Combine retrieved documents into a single prompt
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

# Generate  AI Response
def get_response(user_input:str) -> str:
    """
    Handles the full RAG pipeline:
    retrieval - context injection - answer generation
    """
    docs = st.session_state.vector_store.similarity_search(user_input, k=2)

    if not docs:
        return "⚠️ No relevant information found on the website."
    
    response = st.session_state.rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    return response["answer"]

# Intialize session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history =[
        AIMessage(content="Hi, I'm WebMind AI . Paste a URL in the sidebar and ask me anything about it!")
    ]
if "current_url" not in st.session_state:
    st.session_state.current_url = ""
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None



#Sidebar Website Input
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("Configure your AI assistant")

    website_url = st.text_input("🌐 Website URL",placeholder="https://example.com",
    help="Enter the URL of the website you want to chat with")
       
    if website_url and website_url != st.session_state.current_url:
      with st.spinner("🔄 Loading website..."):
          try:
              vs = get_vectorstore_from_url(website_url)
              rc = build_retriever_chain(vs)
              st.session_state.vector_store = vs
              st.session_state.rag_chain= build_rag_chain(rc)
              st.session_state.current_url = website_url

              st.session_state.chat_history = [
                  AIMessage(content = f"loaded **{website_url}**. What would you like to know?")
                ]
              
              st.sucess("website loaded!")
          except Exception as e:
              st.error(f"Failed to load website url:{e}")

    elif not website_url:
        st.info("Please enter a website URL to get started")
    
    # clear chat button
    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.chat_history = [
            AIMessage(content="chat cleared. Ask me anything about the loaded website!")
        ]
        st.rerun()


#Main Chat Interface
st.title("🧠 **WebMind AI**")
st.markdown("💬 **Ask questions, summarize content, and explore any website using AI-powered retrieval.**")
st.divider()

# Display previous messages
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message.content)
    elif isinstance(message,HumanMessage):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(message.content)

# User input box 
user_query = st.chat_input(
    "Type your message here...",
    disabled = st.session_state.vector_store is None,
)    

# Handle user query
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_query)

    with st.chat_messages("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = get_response(user_query)

        st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response))    