import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from crewai.tools import tool
from src.modules.Pipeline import pipe_eval
from src.modules.DB.chromadb_storing import ChromaDB

@tool('document_retrieval_tool')
def retrieve_information(search_query: str):
    """
    질의어를 입력받아 Vector DB에서 관련 정보를 검색하는 도구.
    """
    pipe = pipe_eval(verbose=True)
    pipe.setup(model='GPT')
    retrieval_result = pipe.Q(search_query, mode='ensemble')
    return retrieval_result
