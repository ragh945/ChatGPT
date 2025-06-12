import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

def build_pdf_vectorstore(uploaded_file, api_key):
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    # Load and split PDF
    loader = PyPDFLoader(temp_path)
    docs = loader.load_and_split()

    # Embed and store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")

    # Retrieval chain
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(
        llm=ChatGroq(api_key=api_key, model="gemma2-9b-it", temperature=0.2),
        retriever=retriever
    )
