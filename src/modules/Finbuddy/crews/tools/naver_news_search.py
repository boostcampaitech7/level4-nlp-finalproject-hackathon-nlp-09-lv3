from crewai.tools import tool
import os
import urllib
import json

@tool('naver_news_search')
def get_news_urls(query:str) :
    """Get news URLs related to a query from the Naver News search engine."""
    client_id = os.environ['NAVER_API_CLIENT_ID']
    client_secret = os.environ["NAVER_API_CLIENT_SECRET"]
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode==200):
        response_body = response.read()
        result = json.loads(response_body) 
        return result['items']
    else:
        print("Error Code:" + rescode)