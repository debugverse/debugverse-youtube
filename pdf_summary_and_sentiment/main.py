from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.pydantic_v1 import BaseModel, Field


class Result(BaseModel):
    """Sentiment result"""
    sentiment: str = Field(description="One sentence summary of the sentiment of the report")
    score: int = Field(description="Sentiment score, ranging from 0 (bearish) to 10 (bullish)")



llm = ChatOllama(
    model="llama3.1:latest",
    temperature=0
)


filename = "ibm.pdf"
loader = PyPDFLoader(file_path=filename)

docs = loader.load()


# Get 10 page content as a string
pages = []
for i in range(2):
    pages.append(docs[i].page_content)
pages = " ".join(pages)


messages = [
    ("system", "You are a helpful assistant that summarizes a PDF. Analyse the document."),
    ("human", pages)
]
print(pages)

structured_llm = llm.with_structured_output(Result)
ai_msg = structured_llm.invoke(messages)

print(ai_msg)