from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='93322594a0fe4dd983dcf87f3090d709')

# /v2/top-headlines

top_headlines = newsapi.get_top_headlines(q='news',
                                          category='business',
                                          language='en',
                                          )

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2021-02-01',
                                      to='2021-02-04',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/sources
sources = newsapi.get_sources()

news_business = []
for article in top_headlines['articles']:
    news_business.append(article['title'])
    print(article['title'])
