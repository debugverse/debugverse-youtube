from langchain_ollama import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.document_transformers import EmbeddingsClusteringFilter
from langchain.embeddings import HuggingFaceBgeEmbeddings

####################
# Code by Debugverse
# https://www.youtube.com/@DebugVerseTutorials
####################


def extract(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=0
    )
    texts = text_splitter.split_documents(pages)
    return texts


def summarize_document_with_kmeans_clustering(file, llm, embeddings):
    filter = EmbeddingsClusteringFilter(embeddings=embeddings, num_clusters=10)

    texts = extract(file)

    try:
        result = filter.transform_documents(documents=texts)
        checker_chain = load_summarize_chain(llm ,chain_type="stuff")
        summary = checker_chain.run(result)
        return summary
    except Exception as e:
        return str(e)
    

model_name = "BAAI/bge-base-en-v1.5"
model_kwargs = {"device": "cuda"} # CUDA for GPU support
encode_kwargs = {"normalize_embeddings": True}

embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

llm = ChatOllama( # Replace with LLM of your choice
    model="llama3.1:latest",
    temperature=0
)

print(summarize_document_with_kmeans_clustering("ibm.pdf", llm, embeddings))