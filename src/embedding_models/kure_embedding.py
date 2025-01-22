from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.base import Embeddings
import torch


def get_text_embedding(text):
    """
    KURE 모델을 사용하여 텍스트 임베딩을 생성합니다.

    Args:
        text (str): 입력 텍스트.

    Returns:
        list: 텍스트 임베딩 벡터. 오류 발생 시 'Error' 문자열 반환.
    """
    try:
        # CUDA 또는 CPU 디바이스 설정
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # KURE 모델과 토크나이저 로드
        tokenizer = AutoTokenizer.from_pretrained("nlpai-lab/KURE-v1")
        model = AutoModel.from_pretrained("nlpai-lab/KURE-v1").to(device)  # 모델을 GPU로 이동

        # 입력 텍스트를 토큰화
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {key: value.to(device) for key, value in inputs.items()}  # 입력 데이터를 GPU로 이동

        # 모델을 통해 임베딩 생성
        with torch.no_grad():
            outputs = model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :]  # [CLS] 토큰의 임베딩 사용

        # 결과를 CPU로 이동 후 리스트 형태로 반환
        return embedding.squeeze().cpu().tolist()

    except Exception as e:
        return f"Error: {str(e)}"



class KURE_EmbeddingModel(Embeddings):
    """Custom embeddings class wrapping the embedding function."""

    def embed_query(self, text: str) -> list[float]:
        return get_text_embedding(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [get_text_embedding(text) for text in texts]
