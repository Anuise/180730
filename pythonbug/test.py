def checkformat(soup, class_tag, data, index, url):
    content = soup.select(class_tag)[index].text
    return content

    date = checkformat(soup, '.article-meta-value', 'date', 3, url)

    #將原始碼做整理
    soup = BeautifulSoup(response.text, 'lxml')
    #content 文章內文
    content = soup.find(id="main-content").text
    target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
    #去除掉 target_content
    content = content.split(target_content)
    #print(content)
    content = content[0].split(date)
    #print(content)
    #去除掉文末 --
    main_content = content[1].replace('--', '')
        #印出內文
    print(main_content)