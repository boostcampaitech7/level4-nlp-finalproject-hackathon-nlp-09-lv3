import torch
from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.base import Embeddings


def get_text_embedding(text):
    """
    KF-DeBERTa 모델을 사용하여 텍스트 임베딩을 생성합니다.

    Args:
        text (str): 입력 텍스트.

    Returns:
        list: 텍스트 임베딩 벡터.
    """
    try:
        # 모델과 토크나이저 불러오기
        tokenizer = AutoTokenizer.from_pretrained("kakaobank/kf-deberta-base")
        model = AutoModel.from_pretrained("kakaobank/kf-deberta-base")

        # 입력 텍스트를 토큰화
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # 모델을 통해 임베딩 생성
        with torch.no_grad():
            outputs = model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :]  # [CLS] 토큰의 임베딩 사용

        # 벡터를 리스트 형태로 반환
        return embedding.squeeze().tolist()

    except Exception as e:
        return f"Error: {str(e)}"


class KF_DeBERTa_EmbeddingModel(Embeddings):
    """Custom embeddings class wrapping the embedding function."""

    def embed_query(self, text: str) -> list[float]:
        return get_text_embedding(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [get_text_embedding(text) for text in texts]
