
import time
import numpy as np
from embedding_models.navercloud_embedding import NaverCloud_EmbeddingModel
from chromadb import Client
from langchain.vectorstores import Chroma




class ChromaDB:
    def __init__(self, collection_name: str):
        """
        Initialize the CSVToChromaDB class.
        
        :param base_dir: The base directory containing the data.
        :param collection_name: The name of the ChromaDB collection.
        """
        self.collection_name = collection_name


    def add_docs(self, documents):
        
        # 한번에 넣으면 오류나서 배치처리
        batch_size = len(documents) // 4
        batches = [
            documents[i * batch_size: (i + 1) * batch_size] for i in range(4)
        ]
        
        if len(documents) % 4 != 0:
            batches[-1].extend(documents[batch_size * 4:])

        if len(documents) <= 100:
            batches = [documents]

        for batch in batches:
            self.db = Chroma.from_documents(
                documents=batch,
                embedding=NaverCloud_EmbeddingModel(),
                collection_name=self.collection_name
            )
            time.sleep(10)
        
    def verify_db(self):
        """
        Verify the data in the ChromaDB collection.
        
        :return: Total number of documents in the collection.
        """
        all_data = self.db.get(include=["documents", "metadatas", "embeddings"])
        total_documents = len(all_data['documents'])
        print(f"Total documents in collection '{self.collection_name}': {total_documents}")
        return self.db
