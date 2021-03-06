from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://nin187:mongolia@cluster0.bx9tr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = client.dbsparta

## HTML을 주는 부분
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/memo", methods=["GET"])
def listing():
    sample_receive = request.args.get("sample_give")
    print(sample_receive)
    return jsonify({"msg": "GET 연결되었습니다!"})


@app.route("/memo", methods=["POST"])
def saving():
    url_receive = request.form["url_give"]
    comment_receive = request.form["comment_give"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    title = soup.select_one('meta[property="og:title"]')["content"]
    image = soup.select_one('meta[property="og:image"]')["content"]
    desc = soup.select_one('meta[property="og:description"]')["content"]

    doc = {
        "title": title,
        "image": image,
        "desc": desc,
        "url": url_receive,
        "comment": comment_receive,
    }
    print(doc)
    db.articles.insert_one(doc)
    return jsonify({"msg": "저장 완료!"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
