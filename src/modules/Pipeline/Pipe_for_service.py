
from DB.chromadb_storing import ChromaDB
import pandas as pd
from utils import get_all_datas, create_documents
import os
from retrievals import bm25, dpr, ensemble
from QA_model import GPTModel
from tqdm import tqdm
from evaluation import G_generation_evaluate, G_retrieval_evaluate

class Pipeline_For_Service:
    def __init__(self, 
                 collection_name = 'chrdb.db',
                 persist_directory = 'modules/DB',
                 mode = 'NaverCloudEmb',
                 topk = 5,
                 verbose = False): 
        self.verbose = verbose
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        folder_name = 'Service_DB_' + mode
        self.topk = topk
        self.model = None

        if os.path.isdir(os.path.join(persist_directory, folder_name)):
            print('생성된 DB가 있어 로드합니다.')
            DB = ChromaDB(collection_name, persist_directory, emb_model = mode, mode = 'service')
            BASE_DIR = './modules/datas' # 데이터가 저장돼 있는 루트를 의미합니다.
            df = get_all_datas(BASE_DIR)
            documents = create_documents(df)
            DB.load_collection()
            self.db = DB.verify_db()
        else:
            print('생성된 DB가 없어 만듭니다.') 
            BASE_DIR = './modules/datas' # 데이터가 저장돼 있는 루트를 의미합니다.
            df = get_all_datas(BASE_DIR)
            documents = create_documents(df)
            DB = ChromaDB(collection_name, persist_directory, emb_model = mode, mode = 'service')
            DB.create_and_add(documents,)
            self.db = DB.verify_db()

        self.DPRRetriever = dpr(self.db, topk = topk)
        self.BM25Retriever = bm25(documents, topk = topk)

        retrievals = [self.DPRRetriever, self.BM25Retriever]
        weights = [0.5, 0.5]
        search_type = 'mmr'
        self.ensemble_retriever = ensemble(retrievals, topk = topk, weights = weights, search_type = search_type)

    def setup(self, model = 'gpt-4o-mini'):
        if model == 'gpt-4o-mini':
            self.model = GPTModel(model_name = 'gpt-4o-mini')
        elif model == 'gpt-4o':
            self.model = GPTModel(model_name = 'gpt-4o')
        self.service_crew = crew_for_service(model = model)

    def Q(self, query: str, mode = 'ensemble'):
        if mode == 'ensemble':
            result = self.ensemble_retriever.invoke(query)
        elif mode == 'bm25':
            result = self.BM25Retriever.invoke(query)
        elif mode == 'dpr':
            result = self.DPRRetriever.invoke(query)
        else:
            print('''가능한 모델을 입력하세용
                    1. ensemble
                    2. bm25
                    3. dpr
                    ''')
            return
        if self.verbose:
            for i in result[:self.topk]:
                print(i)
        return result[:self.topk]
    
    def A(self, query, retrieval_results):

        inputs = {'query' : query, 'paragraphs': [],
                                  'images': {'image_route' : [], 'summary' : []},
                                  'tables': {'table': [], 'summary' : []}, }
        for doc in retrieval_results:
            if doc.metadata['type'] == 'paragraph':
                inputs['paragraphs'].append(doc.metadata['original_content'])

            elif doc.metadata['type'] == 'figure':
                inputs['images']['image_route'].append(doc.metadata['image_route'])
                inputs['images']['summary'].append(doc.page_content)

            elif doc.metadata['type'] == 'table':
                inputs['tables']['table'].append(doc.metadata['table'])
                inputs['tables']['summary'].append(doc.page_content)
                
            else:
                pass
        result = self.service_crew.kickoff(inputs = inputs)
        return result
    
    def QA(self, query:str, mode = 'ensemble'):
        retrieval_results = self.Q(query, mode = mode)
        answer = self.A(query, retrieval_results,)

        return answer