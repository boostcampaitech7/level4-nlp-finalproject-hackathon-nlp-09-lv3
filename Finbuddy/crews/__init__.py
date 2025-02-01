from .crew import Service

# def Get_visual():
#     return Service().processing_crew()
# from .blog_crew import BlogCrew
# from .crew_table_processing import TableProcessingCrew
#from .analysis_crew import AnalysisCrew
from .crew_retrieval import RetrievalCrew
from .crew_test import TestCrew

# def Get_Blog_Crew():
#     return BlogCrew().blog_crew()

# def Get_Table_Crew():
#     return TableProcessingCrew().tableProcessingCrew()

# def Get_Analysis_Crew():
#     return AnalysisCrew().analysis_crew()

# def get_retrieval_crew():
#     return RetrievalCrew().retrieval_crew()

def get_test_crew():
    return TestCrew().test_crew()
