from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote
import json
import requests


authorizeCode = None


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorizeCode

        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.path[7:].encode())
        self.ret = self.path[7:]
        authorizeCode = self.path[7:]


class KakaoTalk(object):
    defaultUrl = "https://m.naver.com/"

    def __init__(self, restKey, redirectUri):
        self.restKey = restKey
        self.redirectUri = redirectUri

    def login_url(self):
        url = "https://kauth.kakao.com/oauth/authorize"
        url += "?client_id={}".format(self.restKey)
        url += "&redirect_uri={}".format(self.redirectUri)
        url += "&response_type=code"
        param = quote(url, safe="")
        return "https://accounts.kakao.com/login?continue={}".format(param)

    def wait_auth(self, port=80, timeout=60):
        httpd = HTTPServer(("0.0.0.0", port), HTTPHandler)
        httpd.timeout = timeout
        httpd.handle_request()
        return authorizeCode

    def user_token(self, code):
        url = "https://kauth.kakao.com/oauth/token"
        data = {}
        data["grant_type"] = "authorization_code"
        data["client_id"] = self.restKey
        data["redirect_uri"] = self.redirectUri
        data["code"] = code
        response = requests.post(url, data=data)
        return json.loads(response.text)["access_token"]

    def get_profile(self, token):
        url = "https://kapi.kakao.com/v1/api/talk/profile"
        headers = {}
        headers["Authorization"] = "Bearer {}".format(token)
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def get_friends(self, token):
        url = "https://kapi.kakao.com/v1/api/talk/friends"
        headers = {}
        headers["Authorization"] = "Bearer {}".format(token)
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def send_text(self, token, text, button="자세히 보기", url=defaultUrl):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {}
        headers["Authorization"] = "Bearer {}".format(token)
        data = {}
        template = {}
        template["object_type"] = "text"
        template["text"] = text
        template["link"] = {"web_url": url, "mobile_web_url": url}
        template["buttons"] = [{"title": button, "link": template["link"]}]
        data["template_object"] = json.dumps(template)
        response = requests.post(url, headers=headers, data=data)
        return json.loads(response.text)

    def send_feed(self, token, title, description, image, url=defaultUrl):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {}
        headers["Authorization"] = "Bearer {}".format(token)
        data = {}
        template = {}
        link = {"web_url": url, "mobile_web_url": url}
        content = {"title": title, "description": description, "image_url": image, "link": link}
        template["object_type"] = "feed"
        template["content"] = content
        data["template_object"] = json.dumps(template)
        response = requests.post(url, headers=headers, data=data)
        return json.loads(response.text)

    def send_list(self, token, header, titles, descriptions, images):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {}
        headers["Authorization"] = "Bearer {}".format(token)
        data = {}
        template = {}
        contents = []
        link = {"web_url": self.defaultUrl, "mobile_web_url": self.defaultUrl}
        for i in range(len(titles)):
            content = {"title": titles[i], "description": descriptions[i], "image_url": images[i], "link": link}
            contents.append(content)
        template["object_type"] = "list"
        template["header_title"] = header
        template["header_link"] = link
        template["contents"] = contents
        data["template_object"] = json.dumps(template)
        response = requests.post(url, headers=headers, data=data)
        return json.loads(response.text)
