from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

def get_rag_chain():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

    llm = ChatGroq(temperature=0.2, groq_api_key="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", model_name="gemma2-9b-it")

    prompt = PromptTemplate.from_template("""
    Use the context below to answer the question:
    Context: {context}
    Question: {question}
    """)
    
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever(), chain_type="stuff")
    return chain
