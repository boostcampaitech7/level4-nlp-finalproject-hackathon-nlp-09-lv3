# from .blog_crew import BlogCrew
# from .crew_table_processing import TableProcessingCrew
#from .analysis_crew import AnalysisCrew
from .crew_retrieval import RetrievalCrew

# def Get_Blog_Crew():
#     return BlogCrew().blog_crew()

# def Get_Table_Crew():
#     return TableProcessingCrew().tableProcessingCrew()

# def Get_Analysis_Crew():
#     return AnalysisCrew().analysis_crew()

def Get_Retrieval_Crew():
    return RetrievalCrew().crew_retrieval()