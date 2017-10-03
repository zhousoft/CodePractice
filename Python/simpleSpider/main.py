#coding:utf-8
import requests
import chardet
import random
import string
import time
from bs4 import BeautifulSoup
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

def downloadHtml(url):
    if url is None:
        return None
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent':user_agent}
    cookis = {'bid': "".join(random.sample(string.ascii_letters + string.digits, 11))}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        res.encoding = chardet.detect(res.content)['encoding']
        return res.text
    print 'request error for ' + res.status_code
    return None

def paeserHtml(html_str, order):
    if html_str is None:
        return None
    soup = BeautifulSoup(html_str, 'lxml' )
    # 取出所有class为info的div
    infos = soup.find_all(class_='info') 
    for index,info in enumerate(infos):
        title = info.find(class_ = 'title').string # 影片名称
        movie_info = info.find('p', class_= '').get_text('\n','</br>') #电影信息
        rating_num = info.find(class_ = 'rating_num').string # 电影评分
        summary_info = info.find(class_ = 'inq') # 电影简介
        if summary_info is not None:
            summary_info = summary_info.string
        print ("排名 %s\n电影名称：%s\n%s\n评分：%s\n简介：%s\n" %(order*25+index+1, title, movie_info, rating_num, summary_info))
        print "======================================"
        

def main():
    for i in range(10):
        url = "https://movie.douban.com/top250?start=%s&filter=" % (25*i)
        content = downloadHtml(url)
        paeserHtml(content, i)
        time.sleep(2)

if __name__ == '__main__':
    main()