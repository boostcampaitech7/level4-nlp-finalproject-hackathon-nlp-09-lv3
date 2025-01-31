from .blog_crew import BlogCrew
from .news_search_crew import NewsCrew

def Get_Blog_Crew():
    return BlogCrew().blog_crew()

def get_news_crew():
    return NewsCrew().news_crew()