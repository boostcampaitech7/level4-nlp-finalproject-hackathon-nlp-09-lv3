import os
import openai
from langchain.embeddings.base import Embeddings
from dotenv import load_dotenv
load_dotenv()
# 환경 변수에서 OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI()

def get_text_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding
    

class OpenAI_EmbeddingModel(Embeddings):

    """Custom embeddings class wrapping the OpenAI embedding function."""
    def embed_query(self, text: str) -> list[float]:
        return get_text_embedding(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [get_text_embedding(text) for text in texts]
