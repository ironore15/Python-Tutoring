import kakaotalk


# 샾 뒤에 적힌 내용은 주석으로, 코드에 영향을 주지 않음
#  따라 적을 필요 X

"""
따옴표 3개로 감싸진 줄들은 전부 주석 처리
test.py의 내용 전체를 실행시키기 싫다면,
실행을 원하지 않는 부분을 따옴표 3개로 감싸서
자신이 원하는 부분만 실행시키세요.
"""

restKey = "00000000000000000000000000000000"    # REST API 키 (자신의 것으로 변경)
redirectUri = "http://127.0.0.1"                # 변경하지 말 것

kt = kakaotalk.KakaoTalk(restKey, redirectUri)
print(kt.login_url())                           # 이 print문은 url을 출력해준다!
authCode = kt.wait_auth(timeout=120)            # timeout은 기본 60초
token = kt.user_token(authCode)
print("token:", token)

# token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# wait_auth와 user_token을 주석 처리한 후,
# 출력된 token의 값을 가지고
# token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# 을 코드에 추가하여 매번 로그인 과정을 하지 않아도 되도록 수정하세요.

profile = kt.get_profile(token)
print(profile)
print(profile["nickName"])
print(profile["profileImageURL"])
print(profile["thumbnailURL"])
print(profile["countryISO"])

text = "대덕고등학교 빛나리 짱짱"
button = "빛나리 바로가기"

print(kt.send_text(token, text, button))

title = "대덕고등학교 빛나리"
description = "#대덕고 #동아리 #공학 #컴퓨터 #코딩 #소프트웨어"
url = "http://daedeokhs.djsch.kr"
image = url + "/images/template/02240/main/m_visual.png"

print(kt.send_feed(token, title, description, image))

header = "교내 과학사진 콘테스트"

titles = ["2017 수상작", "2017 수상작", "2018 수상작"]
descriptions = ["현미경", "생명공학", "물리학"]

url = "http://daedeokhs.djsch.kr/upload/board"

images = []
images.append(url + "/49527/2017/09/1506393205317.jpg")
images.append(url + "/49527/2017/09/1506394483459.jpg")
images.append(url + "/49527/2018/08/1535501219230.jpg")

print(kt.send_list(token, header, titles, descriptions, images))