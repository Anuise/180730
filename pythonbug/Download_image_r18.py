import  requests
from bs4 import BeautifulSoup
import shutil

sesssion = requests.session()   #使用session
url = 'https://www.ptt.cc/ask/over18'   #url中儲存詢問18禁頁面的網址
form_data = {'from' : '/bbs/sex/index.html', 'yes' : 'yes'} #將Form Data中的資料儲存起來
res = sesssion.post(url, data=form_data)    #把form_data的資料post給18禁頁面

def get_articles_content(this_page_article_href):
    image_count = 0
    for url in this_page_article_href:
        r = sesssion.get("https://www.ptt.cc" + url )
        soup = BeautifulSoup(r.text,"html.parser")

        imgs = soup.find_all('a')       #找出所有a標籤（圖片）
        for img in imgs:
            if '.jpg' in img['href']:   #判斷圖片網址是否包含jpg（避免抓錯）
                download_img_from_article(img_url=img['href'], img_name = image_count)  
                #得到圖片連結後丟入download_img_from_article
                print(img['href'])
                image_count += 1


def download_img_from_article(img_url, img_name):
    r = sesssion.get(img_url, stream=True)  #獲取圖片網址
    file_name = str(img_name + 1)   #命名圖片名稱
    print( 'save img to  ./image/'+ file_name + '.jpg')
    try:
        with open('./image/' + file_name + '.jpg', 'wb') as out_file: #使用shutil存圖片,目的地為當前目錄的image資料夾
            shutil.copyfileobj(r.raw, out_file)
    except:
        print('can not save image', img_url)  #失敗印出can not save image
        

def get_all_articles_href(page_url):
    article_href =[]
    r = sesssion.get(page_url)
    soup = BeautifulSoup(r.text,"html.parser")
    results = soup.findAll("div",{"class":"title"})
    for item in results:
        try:
            item_href = item.find("a").attrs["href"]
            article_href.append(item_href)
        except:
            pass
    return article_href


def main_function(url="https://www.ptt.cc/bbs/sex/index.html"):
    r = sesssion.get(url)
    soup = BeautifulSoup(r.text,"html.parser")

    this_page_article_href = get_all_articles_href(page_url=url)
    get_articles_content(this_page_article_href=this_page_article_href)

    btn = soup.select('div.btn-group > a')  #我們用CSS選擇器來解析取得div內class為btn-group下的a標籤
    up_page_href = btn[3]['href']           #回傳的結果「上一頁」在第3個Index,用[‘href’]取得它的href

    next_page_url = 'https://www.ptt.cc' + up_page_href #上一頁的Url放到變數next_page_url內
    main_function(url = next_page_url)
    #Eris Pads Her Chest

main_function()