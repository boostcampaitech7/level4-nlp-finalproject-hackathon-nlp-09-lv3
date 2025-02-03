from DB.chromadb_storing import ChromaDB
from utils import get_all_datas, create_documents
import os
from retrievals import bm25, dpr, ensemble
from tqdm import tqdm
import json
import subprocess
import tempfile

from Finbuddy import crews

def execute_code(code_str: str, ):
    """
    입력받은 파이썬 코드 문자열을 임시 파일에 저장하고 실행하여,
    시각화 이미지를 생성·저장한다.
    input의 ['code'] 부분만을 활용하여 완전한 형태의 코드를 넣어야 한다.
    [경로]
    str: 생성된 이미지 파일의 경로 (예: output/image_name.png)
    """
    
    with open('test.txt', 'w', encoding = 'utf-8') as f:
        f.write(code_str)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
        tmp_file.write(code_str)
        tmp_filename = tmp_file.name

    # 저장된 파일 실행
    try:
        result = subprocess.run(
            ['python', tmp_filename],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"코드 실행 중 오류 발생:\nSTDERR: {e.stderr}\nSTDOUT: {e.stdout}")
    finally:
        # 임시 파일 삭제 (삭제하지 않으려면 주석 처리)
        os.remove(tmp_filename)


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

    def setup(self,):
        self.context_crew = crews.get_context_crew()
        self.image_crew = crews.get_image_crew()
        self.table_crew = crews.get_table_crew()
        self.final_crew = crews.get_final_crew()
        self.news_crew = crews.get_news_crew()

        if not self.verbose:
            for crew in [self.context_crew, self.image_crew, self.table_crew, self.final_crew, self.news_crew]:
                crew.verbose = False
                for agent in crew.agents:
                    agent.verbose = False
                    
        output_dir = "output"
        # 폴더가 없으면 생성
        os.makedirs(output_dir, exist_ok=True)


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
        paragraph = False
        image = False
        table = False
        inputs = {'query' : query, 'paragraphs': [],
                                    'images': {'image_route' : [], 'summary' : []},
                                    'tables': {'table': [], 'summary' : []}, }
        for i, doc in enumerate(retrieval_results):
            if doc.metadata['type'] == 'paragraph':
                inputs['paragraphs'].append(doc.metadata['original_content'])
                paragraph = True

            elif doc.metadata['type'] == 'figure':
                inputs['images']['image_route'].append(doc.metadata['image_route'])
                inputs['images']['summary'].append(doc.page_content)
                image = True

            elif doc.metadata['type'] == 'table':
                inputs['tables']['table'].append(doc.metadata['table'])
                inputs['tables']['summary'].append(doc.page_content)
                table = True
                
            else:
                pass
        if paragraph:
            context_result = self.context_crew.kickoff(inputs = inputs).raw
        else:
            context_result = ''
        if image:
            image_result = self.image_crew.kickoff(inputs = inputs).raw
        else:
            image_result = ''
        if table:
            togle = True
            while togle:
                try:
                    table_result = self.table_crew.kickoff(inputs = inputs)
                    visualize_code = json.loads(table_result.tasks_output[-2].raw)['code']
                    if self.verbose:
                        print(visualize_code)
                    execute_code(visualize_code)
                    table_result = table_result.raw
                    togle = False
                except:
                    togle = True
        else:
            table_result = ''
        final_result = self.final_crew.kickoff(inputs = {'context_result': context_result,
                                                        'table_result' : table_result,
                                                        'image_result' : image_result})
            
        return final_result.raw


    def news_search_A(self, query):
        inputs = {'query': query}
        answer = self.news_crew.kickoff(inputs = inputs)
        return answer.raw
    
    def QA(self, query:str, mode = 'ensemble', search_type = 'closed_domain'):
        if search_type == 'closed_domain':
            A = self.A
            retrieval_results = self.Q(query, mode = mode)
            answer = A(query, retrieval_results,)
        elif search_type == 'open_domain':
            A = self.news_search_A
            answer = A(query)
        return answer


