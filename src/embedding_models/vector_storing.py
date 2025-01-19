import os
import pandas as pd
from embedding_models.navercloud_embedding import get_text_embedding
from chromadb import Client
from chromadb.config import Settings
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


class CSVToChromaDB:
    def __init__(self, base_dir: str, collection_name: str):
        """
        Initialize the CSVToChromaDB class.
        
        :param base_dir: The base directory containing the data.
        :param collection_name: The name of the ChromaDB collection.
        """
        self.base_dir = base_dir
        self.collection_name = collection_name
        self.chroma_client = Client()
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)

    class CustomEmbeddings(Embeddings):
        """Custom embeddings class wrapping the embedding function."""
        def embed_query(self, text: str) -> list[float]:
            return get_text_embedding(text)

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [get_text_embedding(text) for text in texts]

    def process_csv_file(self, csv_path: str):
        """
        Process a single CSV file and add its data to the ChromaDB collection.
        
        :param csv_path: The path to the CSV file.
        """
        try:
            print(f"Processing: {csv_path}")
            df = pd.read_csv(csv_path)

            if 'summary' not in df.columns:
                print(f"Skipping {csv_path}: 'summary' column missing.")
                return

            # Calculate embeddings for each row
            df['embedding'] = df['summary'].apply(lambda text: get_text_embedding(text))

            # Add each row to the collection
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
                        ids=[str(row.get("id", idx))],  # Use row index as fallback for ID
                        embeddings=[row['embedding']]
                    )
                except Exception as e:
                    print(f"Error adding row {idx} from {csv_path}: {e}")
        except Exception as e:
            print(f"Failed to process {csv_path}: {e}")

    def process_all_files(self):
        """
        Process all CSV files in the base directory and add their data to the ChromaDB collection.
        """
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".csv"):
                    csv_path = os.path.join(root, file)
                    self.process_csv_file(csv_path)

        print(f"All data has been processed and added to ChromaDB collection '{self.collection_name}'.")

    def verify_collection(self):
        """
        Verify the data in the ChromaDB collection.
        
        :return: Total number of documents in the collection.
        """
        all_data = self.collection.get(include=["documents", "metadatas", "embeddings"])
        total_documents = len(all_data['documents'])
        print(f"Total documents in collection '{self.collection_name}': {total_documents}")
        return total_documents

    def setup_retrieval(self, embedding_model: Embeddings = None):
        """
        Set up the retrieval system using LangChain and ChromaDB.
        
        :param embedding_model: Custom embedding model to use. Defaults to internal CustomEmbeddings.
        :return: LangChain retriever object.
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
        Query the collection using the retriever and return results.
        
        :param query_text: The query string.
        :param retriever: The LangChain retriever object.
        :return: Retrieved documents.
        """
        results = retriever.get_relevant_documents(query_text)
        return results