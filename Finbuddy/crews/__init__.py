# from .blog_crew import BlogCrew
# from .crew_table_processing import TableProcessingCrew
from .analysis_crew import AnalysisCrew
from tools.register import tool_functions

# def Get_Blog_Crew():
#     return BlogCrew().blog_crew()

# def Get_Table_Crew():
#     return TableProcessingCrew().tableProcessingCrew()

def Get_Analysis_Crew():
    # 예시: AnalysisCrew에서 tool_functions 사용
    crew = AnalysisCrew()
    crew.tools = tool_functions  # tool_functions를 AnalysisCrew 인스턴스에 주입
    return crew.analysis_crew()