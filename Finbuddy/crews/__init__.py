from .blog_crew import BlogCrew
from .crew_table_processing import TableProcessingCrew

def Get_Blog_Crew():
    return BlogCrew().blog_crew()

def Get_Table_Crew():
    return TableProcessingCrew().tableProcessingCrew()