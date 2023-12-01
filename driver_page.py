import time
import traceback

import requests
from bs4 import BeautifulSoup

HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "",
    "DNT": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42"
}

a = requests.get("https://news.mydrivers.com/",
                 headers=HEADER, verify=True, allow_redirects=True)
ids = []
# print(a.content.decode("utf-8"))
# main_page = BeautifulSoup(a.content.decode("utf-8"), "html.parser")
main_page = BeautifulSoup(a.content.decode("utf-8"), "lxml")
n = 1
for i in main_page.find(class_="main_left").find_all("li"):
    try:

        url = i.a["href"]
        __id = url.split("/")[-1].split(".")[0]
        if __id in ids:
            continue
        else:
            ids.append(__id)
        print(__id, i.h3.text, url)
        print("\t", i.p.text.replace("\r\n", ""))
        n += 1
    except:
        pass
print("&" * 20, "get more", "&" * 20)
for loop in range(5):
    print(loop)
    try:
        b = requests.get(
            f"https://blog.mydrivers.com/news/getdatelist20200820.aspx?ac=1&timeks=&timeend=&page={loop + 2}&minid={__id}&callback=NewsList&_={int(time.time() * 1000)}")
        c = b.content.replace(b"NewsList(", b"")[:-1]
        content = eval(c)["data"][0]["html"]
        next = BeautifulSoup(content, "lxml")
        for i in next.find_all("li"):
            try:
                url = i.a["href"]
                __id = url.split("/")[-1].split(".")[0]
                if __id in ids:
                    continue
                else:
                    ids.append(__id)
                print(__id, "[more]{}".format(i.h3.text), url)
                print("\t", i.p.text.replace("\r\n", ""))
            except:
                print(i)
    except Exception as e:
        print(e)
        # print(i)
        # print(next)
        traceback.print_exc()