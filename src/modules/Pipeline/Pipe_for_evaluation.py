
from DB.chromadb_storing import ChromaDB
import pandas as pd
from utils import get_only_paragraphs, create_documents
import os
from retrievals import bm25, dpr, ensemble
from QA_model import GPTModel, Qwen14BModel, Qwen32BModel, ExaoneModel, HyperClovaModel
from tqdm import tqdm
from evaluation import G_generation_evaluate, G_retrieval_evaluate

class Pipeline_For_Eval:
    def __init__(self, 
                 collection_name = 'chrdb.db',
                 persist_directory = 'modules/DB',
                 mode = 'NaverCloudEmb',
                 topk = 3,
                 verbose = False):
        self.verbose = verbose
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        folder_name = 'Eval_DB_' + mode
        self.topk = topk
        self.model = None

        if os.path.isdir(os.path.join(persist_directory, folder_name)):
            print('생성된 DB가 있어 로드합니다.')
            DB = ChromaDB(collection_name, persist_directory, emb_model = mode, mode = 'eval')
            BASE_DIR = './modules/datas' # 데이터가 저장돼 있는 루트를 의미합니다.
            df = get_only_paragraphs(BASE_DIR)
            documents = create_documents(df)
            DB.load_collection()
            self.db = DB.verify_db()
        else:
            print('생성된 DB가 없어 만듭니다.') 
            BASE_DIR = './modules/datas' # 데이터가 저장돼 있는 루트를 의미합니다.
            df = get_only_paragraphs(BASE_DIR)
            documents = create_documents(df)
            DB = ChromaDB(collection_name, persist_directory, emb_model = mode, mode = 'eval')
            DB.create_and_add(documents,)
            self.db = DB.verify_db()


        self.DPRRetriever = dpr(self.db, topk = topk)
        self.BM25Retriever = bm25(documents, topk = topk)

        retrievals = [self.DPRRetriever, self.BM25Retriever]
        weights = [0.5, 0.5]
        search_type = 'mmr'
        self.ensemble_retriever = ensemble(retrievals, topk = topk, weights = weights, search_type = search_type)

    def setup(self, model = 'GPT'):
            if model == 'GPT':
                self.model = GPTModel()
            elif model == 'Qwen14B':
                self.model = Qwen14BModel()
            elif model == 'Qwen32B':
                self.model = Qwen32BModel()
            elif model == 'Exaone':
                self.model = ExaoneModel()
            elif model == 'HyperClova':
                self.model = HyperClovaModel()
            else:
                print('''가능한 모델을 입력하세용
                    1. GPT
                    2. Qwen
                    3. Exaone
                    4. Qwen14B
                    5. Qwen32B
                    ''')
            self.model_name = model
                
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
        retrieval_contents = [doc.metadata['original_content'] for doc in retrieval_results]
        file_names = [doc.metadata['file_name'] for doc in retrieval_results]
        documents = "\n".join(
        [f"{file_names[idx]}: {retrieval_contents[idx].strip()}" for idx in range(len(retrieval_contents))]
        )
        prompt = f"""
참고 문서를 반드시 활용하여 질문에 대한 명확하고 신뢰할 수 있는 답변을 작성하세요.

답변은 300자 이내로 작성하세요.
반드시 질문과 직접적으로 관련된 정보를 제공하세요.
반드시 확실한 정보만 포함하세요.
적절한 세부 정보를 포함하세요.
참고한 문서의 이름을 반드시 명시하세요.

질문: {query.strip()}
참고 문서: {documents}"
정답:"""
        if self.verbose:
            print(prompt)
        prompt.strip()
        answer = self.model.answering(prompt)
        if self.verbose:
            print(answer)
        return answer
    
    def QA(self, query, mode = 'ensemble'):
        retrieval_results = self.Q(query, mode = mode)
        answer = self.A(query, retrieval_results,)
        return answer

    def QA_eval(self, mode = 'ensemble', sampling = True):

        eval_dataset = pd.read_csv('modules/datas/validation_dataset.csv')
        if sampling:
            sample = eval_dataset.sample(1)
            query = sample['question'].values[0]
            ground_truth_answer = sample['answer'].values[0]
        
            retrieval_results = self.Q(query, mode = mode)
            G_retrieval_score = G_retrieval_evaluate(query, retrieval_results)
            generated_answer = self.A(query, retrieval_results)

            G_generation_score = G_generation_evaluate(query, ground_truth_answer, generated_answer)
            if self.verbose:
                print('[query]:', query)
                print('----------'*10)
                print('----------'*10)
                print('[retrieval_results]:', retrieval_results)
                print('----------'*10)
                print('[answer]:', generated_answer)
                print('----------'*10)
                print('[Retrieval score]')
                print(G_retrieval_score)
                print('----------'*10)
                print('[Generation score]')
                print(G_generation_score)
            return generated_answer, G_retrieval_score, G_generation_score
        else:
            self.verbose = False
            generation_scores = []
            retrieval_scores = []
            generated_answers = []
            retrieval_results_list = []
            
            for idx, row in tqdm(eval_dataset.iterrows(), total=len(eval_dataset)):
                query = row['question']
                ground_truth_answer = row['answer']

                retrieval_results = self.Q(query, mode = mode)
                retrieval_results_list.append(retrieval_results)

                G_retrieval_score = G_retrieval_evaluate(query, retrieval_results)
                retrieval_scores.append(G_retrieval_score)

                generated_answer = self.A(query, retrieval_results)
                generated_answers.append(generated_answer)

                G_generation_score = G_generation_evaluate(query, ground_truth_answer, generated_answer)    
                generation_scores.append(G_generation_score)

            eval_dataset['retrieval_results'] = retrieval_results_list
            eval_dataset['generated_answer'] = generated_answers
            eval_dataset['retrieval_score'] = retrieval_scores
            eval_dataset['generation_score'] = generation_scores
            
            print(len(eval_dataset),'에 대한 평가를 마쳤습니다.')
            eval_dataset.to_csv(f'modules/datas/g_eval_result_{self.model_name}_prompt5.csv')
            return eval_dataset