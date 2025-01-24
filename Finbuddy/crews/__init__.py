from .blog_crew import BlogCrew
from .crew_table_processing import TableProcessingCrew
from .analysis_crew import RetrievalAnalysisCrew

def Get_Blog_Crew():
    return BlogCrew().blog_crew()

def Get_Table_Crew():
    return TableProcessingCrew().tableProcessingCrew()

def Get_Analysis_Crew():
    return RetrievalAnalysisCrew().retrieval_analysis_crew()