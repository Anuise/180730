# -*- coding: UTF-8 -*-
import  requests
from bs4 import BeautifulSoup
import shutil


def get_articles_content(this_page_article_href):
    image_count = 0
    for url in this_page_article_href:
        r = requests.get("https://www.ptt.cc" + url )
        soup = BeautifulSoup(r.text,"html.parser")
        # print(soup)
        try:
            author = soup.select('span.article-meta-value')[0].text #作者
            board = soup.select('span.article-meta-value')[1].text  #看板
            title = soup.select('span.article-meta-value')[2].text  #標題
            time = soup.select('span.article-meta-value')[3].text   #時間
            
            push_tag = soup.select('span.push-tag')                 #推文
            push_userid = soup.select('span.push-userid')           #推文id
            push_content = soup.select('span.push-content')         #推文內容
            push_ipdatetime = soup.select('span.push-ipdatetime')   #推文時間
            
            content = soup.find(id="main-content").text             #content 文章內文
            target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'       
            content = content.split(target_content)                 #去除掉 target_content
            content = content[0].split(time)
            main_content = content[1].replace('--','  ')            #去除掉文末 --
            
            print('作者:', author)
            print(board,' 版')
            print('標題:', title)
            print('時間:', time)
            print('內文:', main_content)
            
            push_list_len = len(push_tag)                           #計算推文筆數
            count = 0
            
            while (count < push_list_len):                          #利用迴圈印出所有推文
                print (push_tag[count].text + push_userid[count].text + push_content[count].text + push_ipdatetime[count].text)
                count = count+1
            
            print("=======================分隔線========================")
        except:
            pass
        
        imgs = soup.find_all('a')       #找出所有a標籤（圖片）
        for img in imgs:
            if '.jpg' in img['href']:   #判斷圖片網址是否包含jpg（避免抓錯）
                download_img_from_article(img_url=img['href'], img_name = image_count)  
                #得到圖片連結後丟入download_img_from_article
                print(img['href'])
                image_count += 1


def download_img_from_article(img_url, img_name):
    r = requests.get(img_url, stream=True)
    file_name = str(img_name + 1)
    print( 'save img to  ./image/'+ file_name + '.jpg')
    try:
        with open('/home/au/Pythonpractice-/pythonbug/image/' + file_name + '.jpg', 'wb') as out_file: #下載資料夾寫絕對路徑
            shutil.copyfileobj(r.raw, out_file)
    except:
        print('can not save img', img_url)
        

def get_all_articles_href(page_url):
    article_href =[]
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text,"html.parser")
    results = soup.findAll("div",{"class":"title"})
    for item in results:
        try:
            item_href = item.find("a").attrs["href"]
            article_href.append(item_href)
        except:
            pass
    return article_href


def main_function(url="https://www.ptt.cc/bbs/Beauty/index.html"):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")

    this_page_article_href = get_all_articles_href(page_url=url)
    get_articles_content(this_page_article_href=this_page_article_href)

    btn = soup.select('div.btn-group > a')  #我們用CSS選擇器來解析取得div內class為btn-group下的a標籤
    up_page_href = btn[3]['href']           #回傳的結果「上一頁」在第3個Index,用[‘href’]取得它的href

    next_page_url = 'https://www.ptt.cc' + up_page_href #上一頁的Url放到變數next_page_url內
    main_function(url = next_page_url)
    #Eris Pads Her Chest


main_function()