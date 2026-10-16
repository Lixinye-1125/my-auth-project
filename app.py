from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>我的登录项目</h1><p>第一个网页运行成功！</p>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)