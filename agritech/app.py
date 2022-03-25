from flask import Flask, render_template
from newsapi import NewsApiClient




app = Flask(__name__)


@app.route('/')
def Index():
    newsapi = NewsApiClient(api_key="cfdf4dc189f04b9caf6dfaf8e1c32107")
    #topheadlines = newsapi.get_top_headlines(sources="India.com")
    all_articles = newsapi.get_everything(q='farming, agriculture',
                                      sources='the-times-of-india',
                                      domains='https://timesofindia.indiatimes.com/topic/agriculture/news',
                                      language='en',
                                      sort_by='relevancy',
                                      page_size= 5,
                                      page=1)


    articles = all_articles['articles']

    desc = []
    news = []
    url  = []
    img  = []

    for i in range(len(articles)):
        myarticles = articles[i]


        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        url.append(myarticles['url'])
        img.append(myarticles['urlToImage'])



    #mylist = zip(news, desc, img)
    mylist = zip(news, desc,url,img)


    return render_template('news.html', context = mylist)



@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/qgis')
def qgis():
    return render_template('qgis.html')


if __name__ == "__main__":
    app.run(debug=True)