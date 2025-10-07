import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from PyPDF2 import PdfReader

# Paths
#data_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\Static\academics"
#vector_db_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\VectorDB\academics"

#data_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\Static\admission"
#vector_db_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\VectorDB\admission"

#data_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\Static\Information_For"
#vector_db_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\VectorDB\Information_For"

#data_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\Static\professional_development"
#vector_db_path = r"C:\Users\Zeel Prajapati\Project\PennState\Data\PSUGreatValley\VectorDB\professional_development"

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Step 2: Load and split documents
def load_and_split_documents(directory):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_text = f.read()
                chunks = splitter.split_text(file_text)
                documents.extend(chunks)
            elif file.endswith(".pdf"):
                file_text = extract_text_from_pdf(file_path)
                chunks = splitter.split_text(file_text)
                documents.extend(chunks)
    
    return documents

# Step 3: Create vector database with smaller batches
def create_vector_database(documents, db_path, batch_size=500):
    embeddings = OpenAIEmbeddings()  # Ensure your OpenAI key is set in the environment
    vectordb = Chroma(persist_directory=db_path, embedding_function=embeddings)

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        vectordb.add_texts(batch)  # Add small batches to avoid exceeding the batch limit
    
    vectordb.persist()
    return vectordb

# Execution
print("Loading and splitting documents...")
documents = load_and_split_documents(data_path)
print(f"Total chunks created: {len(documents)}")

print("Creating vector database...")
vector_db = create_vector_database(documents, vector_db_path)
print("Vector database created and stored locally.")
