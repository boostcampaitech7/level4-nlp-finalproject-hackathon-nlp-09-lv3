from DB.chromadb_storing import ChromaDB
from utils import get_all_datas, create_documents
import os
from retrievals import bm25, dpr, ensemble
import shutil
import json
import subprocess
import asyncio
import nest_asyncio
from voice import tts
nest_asyncio.apply()
import tempfile
import unicodedata
from Finbuddy import crews
from QA_model import GPT_Router


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
        self.chat_count = 0
        self.file_names = []
        self.audio_route = None
        self.visualized_name = 'not.png'
        self.reset_output()

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
                    
        output_dir = "./tts_result"
        # 폴더가 없으면 생성
        os.makedirs(output_dir, exist_ok=True)
        output_dir = "./output"
        # 폴더가 없으면 생성
        os.makedirs(output_dir, exist_ok=True)

        
    async def async_multiple_crews(self, paragraph, image, table, inputs):

        context_task = self.context_crew.kickoff_async(inputs=inputs) if paragraph else None
        image_task = self.image_crew.kickoff_async(inputs=inputs) if image else None
        table_task = self.table_crew.kickoff_async(inputs=inputs) if table else None
        
        tasks = tuple(task for task in [context_task, image_task, table_task] if task)
        results = await asyncio.gather(*tasks)
        
        context_result = ''
        image_result = ''
        table_result = ''
        for task in results:
            if task.tasks_output[-1].name == 'context_analysis_task':
                context_result = task
            elif task.tasks_output[-1].name == 'answer_task':
                table_result = task
            elif task.tasks_output[-1].name == 'graph_analysis_task':
                image_result = task
        while table:
            try:
                visualize_code = json.loads(table_result.tasks_output[-2].raw)['code']
                self.visualized_name = json.loads(table_result.tasks_output[-1].raw)['name']
                table_result = table_result.raw
                if self.verbose:
                    print(visualize_code)
                execute_code(visualize_code)
                break  # 성공하면 반복 종료
            except Exception as e:
                if self.verbose:
                    print(f"Error processing table, retrying: {e}")
                table_result = self.table_crew.kickoff(inputs=inputs)
        if not table:
            self.visualized_name = 'not.png'
        
        final_inputs = {"context_result": context_result.raw if context_result != '' else context_result,
                         "image_result": image_result.raw if image_result != '' else image_result,
                           "table_result": table_result}
        final_result = self.final_crew.kickoff(final_inputs)
        return final_result

    def reset_output(self):
        # 삭제할 디렉터리 목록
        output_dirs = ["./output", "./tts_result"]
        
        for output_dir in output_dirs:
            if os.path.exists(output_dir):
                # 폴더 내부의 파일을 개별적으로 삭제
                for file_name in os.listdir(output_dir):
                    file_path = os.path.join(output_dir, file_name)
                    
                    # 'not.png' 파일은 삭제하지 않음
                    if file_name == "not.png":
                        continue
                    
                    # 파일 또는 폴더 삭제
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            else:
                os.makedirs(output_dir, exist_ok=True)

        self.chat_count = 0

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
    
    async def A(self, query, retrieval_results):
        paragraph = False
        image = False
        table = False
        inputs = {'query' : query, 'paragraphs': {'paragraph' : [], 'file_name' : [], 'page': []},
                                    'images': {'image' : [], 'summary' : [], 'file_name' : [], 'page' :[]},
                                    'tables': {'table': [], 'summary' : [], 'file_name': [], 'page': [] }}
        for i, doc in enumerate(retrieval_results):
            if doc.metadata['type'] == 'paragraph':
                inputs['paragraphs']['paragraph'].append(doc.metadata['original_content'])
                inputs['paragraphs']['file_name'].append(unicodedata.normalize("NFD",(doc.metadata['file_name'])))
                inputs['paragraphs']['page'].append(unicodedata.normalize("NFD",doc.metadata['file_name']) + ' - '+ str(doc.metadata['page'])+'페이지')
                paragraph = True

            elif doc.metadata['type'] == 'figure' or doc.metadata['type'] == 'chart' :
                inputs['images']['file_name'].append(unicodedata.normalize("NFD", doc.metadata['file_name']))
                inputs['images']['summary'].append(doc.page_content)
                inputs['images']['page'].append(unicodedata.normalize("NFD",doc.metadata['file_name']) +' - '+ str(doc.metadata['page'])+'페이지')
                image = True

            elif doc.metadata['type'] == 'table':
                inputs['tables']['table'].append(doc.metadata['table'])
                inputs['tables']['summary'].append(doc.page_content)
                inputs['tables']['file_name'].append(unicodedata.normalize("NFD",doc.metadata['file_name']))
                inputs['tables']['page'].append(unicodedata.normalize("NFD",doc.metadata['file_name']) +' - '+ str(doc.metadata['page'])+'페이지')
                table = True
                
            else:
                pass

        final_result = await self.async_multiple_crews(
            paragraph=paragraph, image=image, table=table, inputs=inputs
        )
        file_names_plus_page = set(inputs['paragraphs']['page'] + inputs['images']['page'] + inputs['tables']['page'])
        file_names = set(inputs['paragraphs']['file_name'] + inputs['images']['file_name'] + inputs['tables']['file_name'])
        final_result = final_result.raw
        output_dir = "./tts_result"
        self.audio_route = tts(final_result, save_dir = output_dir, cnt = self.chat_count)  
        final_result = final_result + "\n\n[정보 출처] \n"
        table_str = "\n".join(f"- {file}" 
                            for idx, file in enumerate(file_names_plus_page, start=1))
        

        final_result += table_str
        file_names = list(file_names)
        self.file_names = list(map(lambda x: unicodedata.normalize("NFD",'./modules/datas/pdfs/' + x), file_names))
        for file in file_names:
            if os.path.exists(file):  # 파일이 존재하는지 확인
                shutil.copy(file, output_dir)  # 파일 복사
            else:
                pass

        self.file_names = list(map(lambda x: unicodedata.normalize("NFD",'./modules/datas/pdfs/' + x), file_names))
        self.test = final_result
        self.chat_count += 1


        return final_result, self.file_names, self.audio_route, self.chat_count, self.visualized_name


    def news_search_A(self, query):
        inputs = {'query': query}
        answer = self.news_crew.kickoff(inputs = inputs).raw
        self.file_names = []
        output_dir = "./tts_result"
        self.audio_route = tts(answer, save_dir = output_dir, cnt = self.chat_count)
        self.visualized_name = 'not.png'
        self.chat_count += 1
        return answer
    
    async def QA(self, query:str, mode = 'ensemble', search_type = None):
        router = GPT_Router()
        response = router.answering(query)
        tool = response.tool
        query_or_answer = response.final_answer
        if search_type == 'closed_domain':
            retrieval_results = self.Q(query, mode = mode)
            answer, file_name, audio_route, chat_count, visualized_name = await self.A(query, retrieval_results,)
        elif search_type == 'open_domain':
            answer = self.news_search_A(query_or_answer)
            file_name = self.file_names
            audio_route = self.audio_route
            chat_count = self.chat_count
            visualized_name = self.visualized_name
        else:
            if response.tool == '최신 뉴스기사 검색':
                answer = self.news_search_A(query_or_answer)
                file_name = self.file_names
                audio_route = self.audio_route
                chat_count = self.chat_count
                visualized_name = self.visualized_name

            if tool == '내부 주식 리포트 RAG':
                retrieval_results = self.Q(query, mode = mode)
                answer, file_name, audio_route, chat_count, visualized_name = await self.A(query, retrieval_results,)

            if tool == '직접 답변':
                answer = query_or_answer
                file_name = []
                output_dir = "./tts_result"
                visualized_name = 'not.png'
                self.chat_count += 1
                chat_count = self.chat_count
                audio_route = tts(answer, save_dir = output_dir, cnt = chat_count)

        return answer, file_name, audio_route, chat_count, visualized_name


