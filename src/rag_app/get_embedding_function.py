from langchain_ollama import OllamaEmbeddings
 
def get_embedding_function():
    embeddings=OllamaEmbeddings(model="nomic-embed-text",base_url='http://ollama:11434') 
    return embeddings