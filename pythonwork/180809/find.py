from bs4 import BeautifulSoup
import requests 
from  flask  import  Flask 
import json
import api
import pymongo
import datetime

app  =  Flask ( __name__ )
app.config['JSON_AS_ASCII'] =  False
@app.route ( '/api/<use>/<n>/<number>/' ) 

def  show_user_profile (use, n, number): 
    url1 = 'https://www.ptt.cc/bbs/' +use+ '/index.html'
    m = int(n)
    
    def get_all_articles_href(url, m, number):
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
    
    def get_all_articles_content(this_page_article_href, m, number):
        page_article_href = str(this_page_article_href[m])
        url = page_article_href
        r = requests.get('https://www.ptt.cc' + url)
        soup = BeautifulSoup(r.text,'html.parser')
        try:
            author = soup.select('span.article-meta-value')[0].text
            board = soup.select('span.article-meta-value')[1].text
            title = soup.select('span.article-meta-value')[2].text
            time = soup.select('span.article-meta-value')[3].text

            x = datetime.datetime.now()
            opentime = str(x)
                       
            myclient = pymongo.MongoClient('mongodb://localhost:27017/')
            mydb = myclient["runoobdb"] 
            mycol = mydb["sites"]
            
            count = mycol.find().count()
            id0 = count+1
            print (id0)

            mydata = {
                'id0' : id0,
                'author' : author,
                'board' : board,
                'title' : title,
                'time' : time,
                'opentime' : opentime
            }

            
            y = mycol.insert_one(mydata)
            number0 = int(number)
            myquery = { "id0": number0 }
            mydoc = mycol.find(myquery)
            for data in mycol.find(myquery):
                print(data)
                
            json_data = str(data)
            json_str = json.dumps(json_data, ensure_ascii=False)
            
        except:
            pass

        return json_str

    # def mongo_data(k, number):
    #     myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    #     mydb = myclient["runoobdb"] 
    #     mycol = mydb["sites"]
        
    #     data = eval(k)
    #     x = mycol.insert_one(data)
        
    #     a = 0
    #     # for y in mycol.find():
    #     #     a = a+1
    #     myresult = mycol.find().limit(0)
 
    #     # 输出结果
    #     for x in myresult:
    #         print(x)

    #     return "123"

    
    def main_function(url, m, number):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        this_page_article_href = get_all_articles_href(url, m, number)
        y = get_all_articles_content(this_page_article_href, m, number)
        
        return y
        
    k = main_function(url1, m, number)
    # ans = mongo_data(k, number)
    print('successful')

    return k
    

if  __name__  ==  '__main__' : 
    app.debug  =  True
    app.run ()