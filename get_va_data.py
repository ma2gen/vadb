# 声優の出演作品をニコニコ大百科から取得する

# 機能
# 声優→出演作品　作品→出演声優の検索
# 声優A 声優B の共通出演作品
# 作品A 作品B の共通出演声優の検索
# なお、作品はゲーム、アニメに限定する

# ニコニコのサーバに対して負荷をかけないように、間を置いて検索する

# 1　ニコニコ大百科の声優一覧(男女別)の記事から
# 各声優の記事へのリンクを取得する
# 2　1で取得したリンクから単語「アニメ」「ゲーム」を含む見出しを特定
# 無い場合は「情報なし」を返す
# 3　2で取得したタグの次のタグを調べ、ulタグの内容を取得
# 4　3で取得した内容は、恐らく「'出演作品'('キャラ名')」
# なので「声優名：出演作品（キャラ名）」という形式のデータを作成する

import requests
from bs4 import BeautifulSoup
import csv
import re
import time

def get_urls():
    target_url = "https://dic.nicovideo.jp/a/%E5%A5%B3%E6%80%A7%E5%A3%B0%E5%84%AA%E4%B8%80%E8%A6%A7%28%E4%B8%96%E4%BB%A3%E5%88%A5%29"
    html_doc = requests.get(target_url).text
    soup = BeautifulSoup(html_doc, "html.parser")

    tables = soup.find_all("table")
    with open("female_va_url_list.csv",mode="w",encoding="utf-8") as fp:
        for table in tables:
            links = table.find_all("a")
            for link in links:
                fp.write("{},{}\n".format(link.text, "https://dic.nicovideo.jp"+str(link.get("href"))))

def get_va_detail():
    # get_urls()で作成したcsvからurlのリストを作成
    with open("female_va_url_list.csv",mode="r",encoding="utf-8") as fp:
        reader = csv.reader(fp)
        urls = [row for row in reader]
    
    for url in urls[4:9]:
        print(url[1])
        html_doc = requests.get(url[1]).text
        soup = BeautifulSoup(html_doc, "html.parser")
        works = []
        article = soup.find("div",{"class":"article","id":"article"})
        for ul_tag in article.find_all("ul"):
            for work in ul_tag.find_all("li"):
                works.append(work.text)
        
        for work in works[7:-8]:
            print(work)
        
        """ for work in works:
            print("{}\t{}".format(url[0],work.text)) """
        time.sleep(2)

if __name__ == '__main__':
    #get_urls()
    get_va_detail()