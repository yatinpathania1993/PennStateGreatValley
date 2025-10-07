import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import streamlit as st

# Paths to individual vector databases
vector_db_paths = [
    "C:/Users/Zeel Prajapati/Project/PennState/Data/PSUGreatValley/VectorDB/academics",
    "C:/Users/Zeel Prajapati/Project/PennState/Data/PSUGreatValley/VectorDB/admission",
    "C:/Users/Zeel Prajapati/Project/PennState/Data/PSUGreatValley/VectorDB/professional_development",
    "C:/Users/Zeel Prajapati/Project/PennState/Data/PSUGreatValley/VectorDB/information_for",
]

# Path to the unified vector database
unified_vector_db_path = "C:/Users/Zeel Prajapati/Project/PennState/Data/PSUGreatValley/VectorDB/unified"

# Function to split documents into smaller batches
def batchify(items, batch_size):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

# Combine all vectors into a single database
def combine_vectors(vector_paths, unified_path):
    embeddings = OpenAIEmbeddings()
    unified_db = Chroma(persist_directory=unified_path, embedding_function=embeddings)

    max_batch_size = 5461  # Chroma's batch size limit

    for path in vector_paths:
        # Load the individual vector database
        vector_db = Chroma(persist_directory=path, embedding_function=embeddings)
        
        # Retrieve documents and metadata
        docs = vector_db._collection.get()["documents"]  # Access raw documents
        metadatas = vector_db._collection.get()["metadatas"]

        # Split documents and metadata into smaller batches
        for doc_batch, meta_batch in zip(
            batchify(docs, max_batch_size), batchify(metadatas, max_batch_size)
        ):
            unified_db.add_texts(texts=doc_batch, metadatas=meta_batch)
    
    # Persist the unified database
    unified_db.persist()
    return unified_db

# Combine vectors
print("Combining all vectors into a unified vector database...")
unified_db = combine_vectors(vector_db_paths, unified_vector_db_path)
print("Unified vector database created and persisted.")

# Initialize the unified retrieval agent
retriever = unified_db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
llm = OpenAI()  # Use OpenAI LLM for answering questions

# Create a Retrieval QA chain
unified_qa_agent = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Streamlit App
st.title("Penn State Great Valley Knowledge Base")
st.sidebar.title("About")
st.sidebar.info("This application uses a unified knowledge base to answer queries about Academics, Admission, Professional Development, and Information For.")

# User Input
query = st.text_input("Enter your query:")

if query:
    with st.spinner("Processing your query..."):
        try:
            # Pass the query to the unified QA agent
            response = unified_qa_agent.run(query)
            st.write("### Answer:")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing your query: {str(e)}")
