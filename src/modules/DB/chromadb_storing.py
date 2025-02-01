import time
import os
import numpy as np
from embedding_models.navercloud_embedding import NaverCloud_EmbeddingModel
from embedding_models.kf_deberta_embedding import KF_DeBERTa_EmbeddingModel
from embedding_models.kure_embedding import KURE_EmbeddingModel
from embedding_models.openai_embedding import OpenAI_EmbeddingModel
from chromadb import Client
from langchain_community.vectorstores import Chroma
from langchain.schema import Document 


class ChromaDB:
    def __init__(self, collection_name: str, persist_directory: str, emb_model= 'NaverCloudEmb', mode = 'eval'):
        """
        Initialize the ChromaDB class.
        
        :param collection_name: The name of the ChromaDB collection.
        :param persist_directory: Directory to store the ChromaDB collection.
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        self.db = None
        if mode == 'eval':
            if emb_model == 'NaverCloudEmb':
                self.embedding_function = NaverCloud_EmbeddingModel()
                self.persist_directory += '/Eval_DB_NaverCloudEmb'
            elif emb_model == 'KF_DebertaEmb':
                self.embedding_function = KF_DeBERTa_EmbeddingModel()
                self.persist_directory += '/Eval_DB_KF_DebertaEmb'
            elif emb_model == 'Kure_Emb':
                self.embedding_function = KURE_EmbeddingModel()
                self.persist_directory += '/Eval_DB_Kure_Emb'
            elif emb_model == 'OpenAI_Emb':
                self.embedding_function = OpenAI_EmbeddingModel()
                self.persist_directory += '/Eval_OpenAI_Emb'
            else:
                print('''가능한 임베딩 모델이 아닙니다.
                    [가능한 모델]
                    1. NaverCloudEmb
                    2. KF_DebertaEmb
                    3. Kure_Emb
                    4. OpenAI_Emb''')
                return
        elif mode == 'service':
            if emb_model == 'NaverCloudEmb':
                self.embedding_function = NaverCloud_EmbeddingModel()
                self.persist_directory += '/Service_DB_NaverCloudEmb'
            elif emb_model == 'KF_DebertaEmb':
                self.embedding_function = KF_DeBERTa_EmbeddingModel()
                self.persist_directory += '/Service_DB_KF_DebertaEmb'
            elif emb_model == 'Kure_Emb':
                self.embedding_function = KURE_EmbeddingModel()
                self.persist_directory += '/Service_DB_Kure_Emb'
            elif emb_model == 'OpenAI_Emb':
                self.embedding_function = OpenAI_EmbeddingModel()
                self.persist_directory += '/Service_DB_OpenAI_Emb'
            else:
                print('''가능한 임베딩 모델이 아닙니다.
                    [가능한 모델]
                    1. NaverCloudEmb
                    2. KF_DebertaEmb
                    3. Kure_Emb
                    4. OpenAI_Emb''')
                return
        self.emb_model = emb_model

    def create_and_add(self, documents):
        """
        Add a list of documents to ChromaDB after embedding.
        
        :param documents: List of langchain.schema.Document objects.
        """
        if not isinstance(documents, list) or not all(isinstance(doc, Document) for doc in documents):
            raise ValueError("Input must be a list of langchain.schema.Document objects.")
        
        print(f"Received {len(documents)} documents for embedding.")
        
        # Create ChromaDB collection
        self.db = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
        
        # Add documents in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]

            print(f"Adding batch {i // batch_size + 1} of {len(documents) // batch_size + 1}...")
            self.db.add_documents(batch)
            if self.emb_model == 'NaverCloudEmb':
                time.sleep(5)  # 네이버클라우드 임베딩모델일때만
        
        # Persist the database
        self.db.persist()
        print(f"Collection '{self.collection_name}' created and persisted at '{self.persist_directory}'.")

    def verify_db(self):
        """
        Verify the data in the ChromaDB collection.
        
        :return: Total number of documents in the collection.
        """
        if self.db is None:
            print("No database loaded.")
            return None
        
        try:
            data = self.db.get(include=["documents"])
            total_documents = len(data["documents"])
            print(f"Total documents in collection '{self.collection_name}': {total_documents}")
            return self.db
        except Exception as e:
            print(f"Error during verification: {e}")
            return None

    def load_collection(self):
        """
        Load the ChromaDB collection from disk.
        """
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(f"Persist directory does not exist at: {self.persist_directory}")
        
        self.db = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
        print(f"Collection '{self.collection_name}' loaded from '{self.persist_directory}'.")
        return self.db
