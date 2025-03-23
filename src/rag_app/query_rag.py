from dataclasses import dataclass
from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from rag_app.get_chroma_db import get_chroma_db
    


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

@dataclass
class QueryResponse:
     query_text: str
     response_text: str
     sources: List[str]
 
def query_rag(query_text: str) -> QueryResponse:
    db = get_chroma_db()

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOllama(model="llama3.2",base_url='http://ollama:11434')

    response = model.invoke(prompt)

    response_text = response.content
 
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")
 
    return QueryResponse(
         query_text=query_text, response_text=response_text, sources=sources
     )
 
if __name__ == "__main__":
    query_rag("What is DBMS")