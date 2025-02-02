from newspaper import Article

from crewai.tools import tool

@tool('urls_to_context')
def get_article(urls:list):
    """Get news contexts from URLs"""
    result = {'title': [], 'context': []}
    for url in urls:
        # 기사 객체 생성
        try:
            article = Article(url)

            # 기사 다운로드 및 파싱
            article.download()
            article.parse()

            # 본문 내용 추출
            result['title'].append(article.title)
            result['context'].append(article.text)
        except:
            pass
    return result
