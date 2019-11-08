from bs4 import BeautifulSoup
import requests

url = 'http://daedeokhs.djsch.kr'
path = '/schedule/list.do'
query = 's=taedokhs&schdYear=2019&schdMonth=11'
r = requests.get(url + path + '?' + query)

index = r.text.find('<th scope="row"')
while index != -1:                          # 검색에 실패할 때까지
    final_index = r.text.find("</th>", index)
    print(r.text[index:final_index+5])
    next_index = r.text.find('<th scope="row"', index + 1)      # find의 두 번째 인자는 start index
    title_start = r.text.find('title="', index, next_index)     # find의 세 번째 인자는 end index
    if title_start != -1:
        title_end = r.text.find('"', title_start + 7)
        print(r.text[title_start+7:title_end])
    index = next_index


path = '/boardCnts/list.do'
query = 'boardID=49529&m=040602&s=taedokhs'

r = requests.get(url + path + '?' + query)
print(r.text)

index = r.text.find('/upload/board/49529/')
while index != -1:
    final_index = r.text.find('.jpg', index)
    image_path = r.text[index:final_index+4]

    image_path = image_path.replace('/thumb/', '/')
    new_r = requests.get(url + image_path)
    with open(str(index) + '.jpg', 'wb') as f:
        f.write(new_r.content)

    index = r.text.find('/upload/board/49529/', index + 1)