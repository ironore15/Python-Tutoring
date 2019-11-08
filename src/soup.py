from bs4 import BeautifulSoup
import requests


url = 'http://daedeokhs.djsch.kr'
path = '/schedule/list.do'
query = 's=taedokhs&schdYear=2019&schdMonth=11'
r = requests.get(url + path + '?' + query)

bs = BeautifulSoup(r.text, "html.parser")
trs = bs.findAll("tr")
for tr in trs:
    th = tr.find("th", {"scope": "row"})
    if th:
        print(th.get_text())
        a = tr.find("a")
        if a:
            print(a.get_text())


path = '/boardCnts/list.do'
query = 'boardID=49529&m=040602&s=taedokhs'

r = requests.get(url + path + '?' + query)
bs = BeautifulSoup(r.text, "html.parser")

date = "11월7일"
img = bs.find("img", {"alt": date + "(중/석식) 사진"})
img_path = img["src"].replace("/thumb/", "/")

r = requests.get(url + img_path)
with open(date + ".jpg", "wb") as f:
    f.write(r.content)