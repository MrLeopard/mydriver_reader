"""
Autor   : Mr Leopard
License : MIT
"""

import copy
import time
import requests
from bs4 import BeautifulSoup

_HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/webp,image/apng,*/*;"
              "q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "",
    "DNT": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42"
}


class Provider(object):
    def __init__(self):
        self.cursor = None
        self.loop = 0
        self.content = {
            "index": -1,
            "id": [],
            "datas": []
        }

    def get_dozen(self, direction="next"):
        if len(self.content["datas"]) == -1:  # 刚启动，或者清空过
            self.__get_one_page()
            self.content["index"] = 0
            return self.content["datas"][self.content["index"]]

        if direction == "next":
            if len(self.content["datas"]) > self.content["index"] + 1:
                self.content["index"] += 1
            else:
                self.__get_one_page()
                self.content["index"] += 1
        elif direction == "previous":
            if self.content["index"] == 0:
                pass
            else:
                self.content["index"] -= 1

        return self.content["datas"][self.content["index"]]

    def __get_one_page(self):
        if not self.cursor:
            __url = f"https://blog.mydrivers.com/news/getdatelist20200820.aspx?"
        else:
            __url = f"https://blog.mydrivers.com/news/getdatelist20200820.aspx?" \
                    f"ac=1&timeks=&timeend=&page={self.loop + 2}&minid={self.cursor}&" \
                    f"callback=NewsList&_={int(time.time() * 1000)}"

        resp = requests.get(__url, headers=_HEADER, verify=True, allow_redirects=True)
        c = resp.content.replace(b"NewsList(", b"")[:-1]
        content = eval(c)["data"][0]["html"]
        news = BeautifulSoup(content, "lxml").find_all("li")
        page_content = []
        for i in news:
            try:
                __url = i.a["href"]
                __id = __url.split("/")[-1].split(".")[0]
                __time = i.span.text
                __title = i.h3.text
                if __id in self.content["id"]:
                    continue
                else:
                    self.content["id"].append(__id)
                    page_content.append({"id": __id,
                                         "time": __time,
                                         "title": __title,
                                         "url": __url})
                self.cursor = __id
            except:
                if "display: none;" not in str(i):
                    print(repr(i), "errors")
        self.content["datas"].append(page_content)
        self.loop += 1

        return page_content

    def clear(self):
        self.loop = 0
        self.content = {
            "index": -1,
            "id": [],
            "datas": []
        }

    def get_new_content_text(self, info: dict):
        __e = None
        text = []
        for _i in range(5):
            try:
                __resp = requests.get(info["url"], headers=_HEADER, verify=True, allow_redirects=True)
                break
            except Exception as e:
                __e = copy.deepcopy(e)
                time.sleep(0.2)
        else:
            print(__e)
            return text
        __page = BeautifulSoup(__resp.content, "lxml")
        content = __page.find(class_="news_info")

        for p in content.find_all("p"):
            __text = p.text.strip()
            if __text:
                if "【本文结束】" in __text or "责任编辑" in text:
                    break
                text.append(__text)
        return text


if __name__ == "__main__":
    p = Provider()
    print(p.get_dozen())
