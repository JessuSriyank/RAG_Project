import os
import time
# from dotenv import load_dotenv
from pyngrok import ngrok
import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
groq_api_key="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"

# Set up Streamlit
st.title("RAG Application")


def hide_streamlit_style():
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )


hide_streamlit_style()

# Initialize the language model
try:
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
except Exception as e:
    st.error(f"Error initializing ChatGroq model: {e}")
    st.stop()

# File upload for PDF
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

# Process PDF and create vector store
if uploaded_file:
    try:
        # Save uploaded file
        with open("uploaded_document.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Initialize embeddings and document loader
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        loader = PyPDFLoader("uploaded_document.pdf")
        docs = loader.load()

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        final_documents = text_splitter.split_documents(docs[:20])

        # Create FAISS vector store
        vectors = FAISS.from_documents(final_documents, embeddings)
        retriever = vectors.as_retriever()

        # Define retrieval prompt template
        prompt_template = ChatPromptTemplate.from_template(
            """
            Answer the question based on the provided context only.
            Please provide the most accurate response based on the question.
            <context>
            {context}
            <context>
            Question: {input}
            """
        )

        # Set up document chain and retrieval chain
        document_chain = create_stuff_documents_chain(llm, prompt_template)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        st.stop()

    # Get user query
    user_query = st.text_input("Enter your question here:")

    if user_query:
        try:
            start = time.process_time()
            response = retrieval_chain.invoke({"input": user_query})
            end_time = time.process_time() - start

            st.write(f"Response time: {end_time:.2f} seconds")
            st.subheader("AI Response:")
            st.write(response.get('answer', "No response generated."))

            # Display retrieved documents with similarity search
            context_results = response.get("context", [])
            if context_results:
                with st.expander("Document Similarity Search Results"):
                    for i, doc in enumerate(context_results):
                        st.write(f"**Result {i + 1}:**")
                        st.write(doc.page_content)
                        st.write("--------------------------------")
        except Exception as e:
            st.error(f"Error during query processing: {e}")
else:
    st.warning("Please upload a PDF file to start.")
