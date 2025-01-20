import os
import pandas as pd
from embedding_models.navercloud_embedding import get_text_embedding, process_csv_and_generate_embeddings
from chromadb import Client
from chromadb.config import Settings
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


class CSVToChromaDB:
    def __init__(self, base_dir: str, collection_name: str):
        """
        CSVToChromaDB 클래스를 초기화합니다.
        
        :param base_dir: 데이터를 포함하는 기본 디렉토리 경로입니다.
        :param collection_name: ChromaDB 컬렉션의 이름입니다.
        """
        self.base_dir = base_dir
        self.collection_name = collection_name
        self.chroma_client = Client()
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)

    class CustomEmbeddings(Embeddings):
        """임베딩 함수를 래핑한 커스텀 임베딩 클래스입니다."""
        def embed_query(self, text: str) -> list[float]:
            return get_text_embedding(text)

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [get_text_embedding(text) for text in texts]

    def process_csv_file(self, csv_path: str, output_path: str):
        """
        process_csv_and_generate_embeddings 함수를 사용하여 CSV 파일을 처리하고,
        ChromaDB 컬렉션에 데이터를 추가합니다.

        :param csv_path: 입력 CSV 파일 경로입니다.
        :param output_path: 임베딩이 포함된 처리된 CSV를 저장할 경로입니다.
        """
        try:
            # 외부 임베딩 처리 함수 호출
            process_csv_and_generate_embeddings(csv_path, output_path)

            # 임베딩이 포함된 CSV 파일 불러오기
            df = pd.read_csv(output_path)

            # 컬렉션에 각 행 추가
            for idx, row in df.iterrows():
                try:
                    self.collection.add(
                        documents=[row['summary']],
                        metadatas={
                            "id": row.get("id"),
                            "type": row.get("type"),
                            "image_route": row.get("image_route"),
                            "dir_route": row.get("dir_route"),
                            "file_name": row.get("file_name"),
                            "page": row.get("page"),
                            "investment": row.get("investment"),
                            "company_name": row.get("company_name"),
                            "table": row.get("table"),
                            "original_content": row.get("original_content"),
                        },
                        ids=[str(row.get("id", idx))],  # ID로 행 인덱스를 대체
                        embeddings=eval(row['embedding']) # 문자열로 저장된 리스트를 리스트로 변환
                    )
                except Exception as e:
                    print(f"{csv_path}에서 {idx}번째 행 추가 중 오류 발생: {e}")
        except Exception as e:
            print(f"{csv_path} 처리 실패: {e}")

    def process_all_files(self, output_dir: str):
        """
        기본 디렉토리에 있는 모든 CSV 파일을 처리하고,
        해당 데이터를 ChromaDB 컬렉션에 추가합니다.

        :param output_dir: 임베딩이 포함된 처리된 CSV 파일을 저장할 디렉토리입니다.
        """
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".csv"):
                    csv_path = os.path.join(root, file)
                    output_path = os.path.join(output_dir, f"processed_{file}")
                    self.process_csv_file(csv_path, output_path)

        print(f"모든 데이터가 처리되어 ChromaDB 컬렉션 '{self.collection_name}'에 추가되었습니다.")

    def verify_collection(self):
        """
        ChromaDB 컬렉션에 있는 데이터를 확인합니다.
        
        :return: 컬렉션에 있는 총 문서 수입니다.
        """
        all_data = self.collection.get(include=["documents", "metadatas", "embeddings"])
        total_documents = len(all_data['documents'])
        print(f"컬렉션 '{self.collection_name}'에 있는 문서 총 개수: {total_documents}")
        return total_documents

    def setup_retrieval(self, embedding_model: Embeddings = None):
        """
        LangChain과 ChromaDB를 사용하여 검색 시스템을 설정합니다.
        
        :param embedding_model: 사용할 커스텀 임베딩 모델입니다. 기본값은 내부 CustomEmbeddings입니다.
        :return: LangChain의 retriever 객체를 반환합니다.
        """
        if embedding_model is None:
            embedding_model = self.CustomEmbeddings()

        vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=embedding_model,
            client=self.chroma_client,
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Retrieve top 5 results
        return retriever

    def query(self, query_text: str, retriever):
        """
        검색기를 사용하여 컬렉션에서 쿼리를 수행하고 결과를 반환합니다.
        
        :param query_text: 검색할 쿼리 문자열입니다.
        :param retriever: LangChain의 retriever 객체입니다.
        :return: 검색된 문서들입니다.
        """
        results = retriever.get_relevant_documents(query_text)
        return results