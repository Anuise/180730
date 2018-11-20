import shutil   #安裝shutil套件
import requests #安裝requests套件

img_url = 'https://i.imgur.com/5EleFNS.jpg' #輸入圖片url
img_name = 'img'    #命名圖片名稱
r = requests.get(img_url, stream = True) #獲取圖片網址
print('save img to ./image/' + img_name +'.jpg')

with open('./image/' + img_name + '.jpg', 'wb') as out_file:    
    shutil.copyfileobj(r.raw, out_file)
#使用shutil存圖片,目的地為當前目錄的image資料夾