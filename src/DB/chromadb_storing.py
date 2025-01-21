import time
import os
import numpy as np
from embedding_models.navercloud_embedding import NaverCloud_EmbeddingModel
from chromadb import Client
from langchain.vectorstores import Chroma
from langchain.schema import Document 


class ChromaDB:
    def __init__(self, collection_name: str, persist_directory: str):
        """
        Initialize the ChromaDB class.
        
        :param collection_name: The name of the ChromaDB collection.
        :param persist_directory: Directory to store the ChromaDB collection.
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.db = None

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
            embedding_function=NaverCloud_EmbeddingModel()
        )
        
        # Add documents in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            print(f"Adding batch {i // batch_size + 1} of {len(documents) // batch_size + 1}...")
            self.db.add_documents(batch)
            time.sleep(5)  # To ensure stability during persistence
        
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
            return total_documents
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
            embedding_function=NaverCloud_EmbeddingModel()
        )
        print(f"Collection '{self.collection_name}' loaded from '{self.persist_directory}'.")

