from crewai.tools import tool
from langchain.tools import DuckDuckGoSearchRun

@tool('duckduckgosearch')
def search(search_query:str):
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(search_query)
