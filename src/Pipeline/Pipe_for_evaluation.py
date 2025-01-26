from DB.chromadb_storing import ChromaDB
import pandas as pd
from utils import get_only_paragraphs, get_all_datas, create_documents
import os
from retrievals import bm25, dpr, ensemble
from QA_model.exaone_model import ExaoneModel
from QA_model.qwen_model import QwenModel
from QA_model.gpt_model import GPTModel
from evaluation import G_evaluate

class Pipeline_For_Eval:
    def __init__(self, 
                 collection_name = 'chrdb.db',
                 persist_directory = 'DB',
                 mode = 'NaverCloudEmb',
                 topk = 5,
                 verbose = False):
        self.verbose = verbose
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        folder_name = 'DB' + '_' + mode
        self.topk = topk
        if os.path.isdir(os.path.join(persist_directory, folder_name)):
            print('생성된 DB가 있어 로드합니다.')
            DB = ChromaDB(collection_name, persist_directory, mode = mode)
            BASE_DIR = './datas' # 데이터가 저장돼 있는 루트를 의미합니다.
            df = get_only_paragraphs(BASE_DIR)
            documents = create_documents(df)
            DB.load_collection()
            self.db = DB.verify_db()
        else:
            print('생성된 DB가 없어 만듭니다.') 
            BASE_DIR = './datas' # 데이터가 저장돼 있는 루트를 의미합니다.
            df = get_only_paragraphs(BASE_DIR)
            documents = create_documents(df)
            DB = ChromaDB(collection_name, persist_directory, mode = mode)
            DB.create_and_add(documents,)
            self.db = DB.verify_db()


        self.DPRRetriever = dpr(self.db, topk = topk)
        self.BM25Retriever = bm25(documents, topk = topk)

        retrievals = [self.DPRRetriever, self.BM25Retriever]
        weights = [0.5, 0.5]
        search_type = 'mmr'
        self.ensemble_retriever = ensemble(retrievals, topk = topk, weights = weights, search_type = search_type)

    
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
    
    def A(self, query, retrieval_results, model = 'GPT'):
        retrieval_results = [doc.metadata['original_content'] for doc in retrieval_results]
        documents = "\n".join(
        [f"참고 문서{idx + 1}: {doc.strip()}" for idx, doc in enumerate(retrieval_results)])
        prompt = f"""
주어지는 참고 문서들을 반드시 활용하여 질문에 100자 이내의 정답을 말하세요.
질문: {query.strip()}
{documents}
정답:"""
        if self.verbose:
            print(prompt)
        if model == 'GPT':
            model = GPTModel()
        elif model == 'Qwen':
            model = QwenModel()
        elif model == 'Exaone':
            model = ExaoneModel()
        else:
            print('''가능한 모델을 입력하세용
                  1. GPT
                  2. Qwen
                  3. Exaone
                  ''')
            return
        prompt.strip()
        answer = model.answering(prompt)
        if self.verbose:
            print(answer)
        return answer
    
    def QA(self, query, mode = 'ensemble', model = 'GPT'):
        retrieval_results = self.Q(query, mode = mode)
        answer = self.A(query, retrieval_results, model = model)
        return answer

    def QA_eval(self, mode = 'ensemble', model = 'GPT'):
        eval_dataset = pd.read_csv('datas/validation_dataset.csv')
        sample = eval_dataset.sample(1)
        query = sample['question'].values[0]
        print('[query]:', query)
        print('----------'*10)
        ground_truth_answer = sample['answer'].values[0]
        
        retrieval_results = self.Q(query, mode = mode)
        answer = self.A(query, retrieval_results, model = model)
        score = G_evaluate(query, retrieval_results, ground_truth_answer, answer)
        if self.verbose:
            print('----------'*10)
            print('[answer]:', answer)
            print('----------'*10)
            print('[score]')
            print(score)
        return answer, score