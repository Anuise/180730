from bs4 import BeautifulSoup
import requests 
from  flask  import  Flask 
import json
import api
import pymongo
app  =  Flask ( __name__ )
app.config['JSON_AS_ASCII'] =  False
@app.route ( '/api/<use>/<n>' ) 

def  show_user_profile (use, n): 
    url1 = 'https://www.ptt.cc/bbs/' +use+ '/index.html'
    m = int(n)

    def get_all_articles_href(url, m):
        article_href = []
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        results = soup.findAll('div',{'class':'title'})
        for item in results:
            try:
                item_href = item.find('a').attrs['href']
                article_href.append(item_href)
                
            except:
                pass
        return article_href
    
    def get_all_articles_content(this_page_article_href, m):
        page_article_href = str(this_page_article_href[m])
        url = page_article_href
        r = requests.get('https://www.ptt.cc' + url)
        soup = BeautifulSoup(r.text,'html.parser')
        try:
            author = soup.select('span.article-meta-value')[0].text
            board = soup.select('span.article-meta-value')[1].text
            title = soup.select('span.article-meta-value')[2].text
            time = soup.select('span.article-meta-value')[3].text

            myclient = pymongo.MongoClient('mongodb://localhost:27017/')
            mydb = myclient["runoobdb"] 
            mycol = mydb["sites"]

            mydata = {
                'author' : author,
                'board' : board,
                'title' : title,
                'time' : time
            }
            
            josn_str = json.dumps(mydata, ensure_ascii=False)

            

            x = mycol.insert_one(mydata)

        except:
            pass

        return josn_str

    def main_function(url, m):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        this_page_article_href = get_all_articles_href(url, m)

        y = get_all_articles_content(this_page_article_href, m)

        
        return y
        
    k = main_function(url1, m)
    print('successful')
    return  k

if  __name__  ==  '__main__' : 
    app.debug  =  True
    app.run ()