import chromadb
import csv
import os
from embedding_models.navercloud_embedding import get_text_embedding
from langchain.embeddings.base import Embeddings


class EmbeddingProcessor(Embeddings):
    def embed_query(self, query: str) -> list:
        return get_text_embedding(query)
    
    def embed_documents(self, documents: list) -> list:
        return [get_text_embedding(doc) for doc in documents]


class ChromaDBHandler:
    """
    ChromaDB와의 상호작용을 담당하는 클래스입니다.
    """
    def __init__(self, collection_name: str):
        # ChromaDB 클라이언트를 초기화하고, 지정된 컬렉션을 불러옵니다.
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(collection_name)
    
    def add_document(self, document: str, embedding: list, metadata: dict):
        """
        텍스트 문서와 임베딩 벡터, 메타데이터를 ChromaDB에 추가합니다.
        """
        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            embeddings=[embedding]
        )
    
    def get_all_documents(self):
        """
        컬렉션에서 모든 문서를 조회하여 반환합니다.
        """
        return self.collection.get()


class CSVProcessor:
    """
    CSV 파일을 처리하고, 데이터를 ChromaDB에 추가하는 클래스입니다.
    """
    def __init__(self, embedding_processor: EmbeddingProcessor, db_handler: ChromaDBHandler):
        self.embedding_processor = embedding_processor
        self.db_handler = db_handler
    
    def process_csv_file(self, file_path: str):
        """
        단일 CSV 파일을 처리하여 문서를 ChromaDB에 추가합니다.
        """
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                summary = row['summary']
                embedding = self.embedding_processor.embed_query(summary)
                
                # 메타데이터 필드 추가
                metadata = {
                    'id': row['id'],
                    'type': row['type'],
                    'image_route': row['image_route'],
                    'dir_route': row['dir_route'],
                    'file_name': os.path.basename(file_path),
                    'page': row['page'],
                    'investment': row['investment'],
                    'company_name': row['company_name'],
                    'table': row['table'],
                    'original_content': row['original_content']
                }
                
                # 문서 추가
                self.db_handler.add_document(summary, embedding, metadata)
    
    def process_all_files(self, directory_path: str):
        """
        지정된 디렉토리 및 하위 디렉토리 내 모든 CSV 파일을 처리하여 데이터를 ChromaDB에 추가합니다.
        """
        # os.walk()를 사용하여 모든 하위 디렉토리와 파일을 순회
        for root, _, files in os.walk(directory_path):
            for filename in files:
                if filename.endswith('.csv'):
                    # 각 CSV 파일의 전체 경로 생성
                    file_path = os.path.join(root, filename)
                    self.process_csv_file(file_path)


class Retriever:
    """
    ChromaDB에서 관련 문서를 검색하는 클래스를 정의합니다.
    """
    def __init__(self, db_handler: ChromaDBHandler, embedding_processor: EmbeddingProcessor):
        self.db_handler = db_handler
        self.embedding_processor = embedding_processor
    
    def setup_retrieval(self):
        """
        LangChain을 사용하여 ChromaDB와 연결된 검색 시스템을 설정합니다.
        """
        # ChromaDB에서 벡터 저장소를 불러오기
        vectorstore = chromadb.Chroma.from_documents(self.db_handler.get_all_documents()['documents'], self.embedding_processor)
        
        # LangChain의 retriever 설정 (k=5로 상위 5개 문서 반환)
        retriever = vectorstore.as_retriever(k=5)
        return retriever
    
    def query(self, query: str):
        """
        사용자가 입력한 쿼리 텍스트에 대해 관련된 문서를 검색하여 반환합니다.
        """
        retriever = self.setup_retrieval()
        result = retriever.get_relevant_documents(query)
        return result


def main():
    """
    전체 시스템 흐름을 실행하는 함수입니다.
    """
    # 각 클래스 인스턴스 생성
    embedding_processor = EmbeddingProcessor()
    db_handler = ChromaDBHandler(collection_name="documents")
    csv_processor = CSVProcessor(embedding_processor, db_handler)
    retriever = Retriever(db_handler, embedding_processor)

    # 지정된 디렉토리에서 CSV 파일 처리
    csv_processor.process_all_files('/path/to/csv_files')

    # 예시 쿼리 실행
    query = "특정 텍스트에 대한 검색 쿼리"
    results = retriever.query(query)

    # 검색 결과 출력
    for result in results:
        print(result)


# 실행
if __name__ == "__main__":
    main()
