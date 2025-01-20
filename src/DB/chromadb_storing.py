import time
import os
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
        # self.base_dir = base_dir
        self.collection_name = collection_name
        self.chroma_client = Client()
        self.db = None

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

    def save_collection(self, save_dir="/data/ephemeral/home/level4-nlp-finalproject-hackathon-nlp-09-lv3/data/db"):
        """
        Save the current ChromaDB collection to disk.
        
        :param save_dir: Directory where the collection will be saved.
        """
        if self.db is None:
            raise ValueError("No database loaded to save. Please add documents first.")
        
        save_path = os.path.join(save_dir, self.collection_name)
        os.makedirs(save_path, exist_ok=True)
        
        # Set the persist directory
        self.db.persist_directory = save_path

        # Call persist without arguments
        self.db.persist()
        print(f"Collection '{self.collection_name}' saved at: {save_path}")
    
    def load_collection(self, load_dir="/data/ephemeral/home/level4-nlp-finalproject-hackathon-nlp-09-lv3/data/db"):
        """
        Load a ChromaDB collection from disk.
        
        :param load_dir: Directory where the collection is saved.
        """
        load_path = os.path.join(load_dir, self.collection_name)
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"Collection directory does not exist at: {load_path}")
        
        self.db = Chroma(
            persist_directory=load_path,
            embedding_function=NaverCloud_EmbeddingModel()
        )
        print(f"Collection '{self.collection_name}' loaded from: {load_path}")
