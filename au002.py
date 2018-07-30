import requests
from bs4 import BeautifulSoup
r = requests.get("https://www.ptt.cc/bbs/ToS/M.1529295126.A.E4C.html")
soup = BeautifulSoup(r.text,"html.parser")

author = soup.select('span.article-meta-value')[0].text
board = soup.select('span.article-meta-value')[1].text
title = soup.select('span.article-meta-value')[2].text
time = soup.select('span.article-meta-value')[3].text
print('作者:', author)
print(board,' 看版')
print('標題:', title)
print('時間:', time)

import csv

# table = [
#     ['作者:',' 看版','標題:','時間:'],
#     [author,board,title,time]
    
#]

with open('c1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['作者:',' 看版','標題:','時間:'])
    writer.writerow([author,board,title,time])  
