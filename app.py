from contextlib import closing
from pathlib import Path
import re
import secrets
import sqlite3

from flask import Flask, flash, redirect, render_template_string, request, url_for
from flask_wtf.csrf import CSRFError, CSRFProtect
from werkzeug.security import generate_password_hash

app = Flask(__name__)
data_dir = Path(app.instance_path)
data_dir.mkdir(parents=True, exist_ok=True)

# 密钥和数据库保存在已被 Git 忽略的 instance 文件夹中。
key_file = data_dir / "secret.key"
if not key_file.exists():
    key_file.write_text(secrets.token_hex(32), encoding="utf-8")

app.config.update(
    SECRET_KEY=key_file.read_text(encoding="utf-8"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=16 * 1024,
)
CSRFProtect(app)
database = data_dir / "users.db"

with closing(sqlite3.connect(database)) as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    db.commit()

REGISTER_PAGE = """
<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>注册账号</title>
<body style="max-width:420px;margin:60px auto;padding:20px;font-family:sans-serif">
<h1>注册账号</h1>
<p>用户名：3—30 位英文字母、数字或下划线；字母统一转为小写。</p>
<p>密码：12—128 个字符。</p>
{% for message in get_flashed_messages() %}<p>{{ message }}</p>{% endfor %}
{% if error %}<p role="alert">{{ error }}</p>{% endif %}
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <p><label>用户名<br><input name="username" required minlength="3"
        maxlength="30" pattern="[A-Za-z0-9_]+" autocomplete="username"></label></p>
    <p><label>密码<br><input name="password" type="password" required
        minlength="12" maxlength="128" autocomplete="new-password"></label></p>
    <button type="submit">注册</button>
</form>
</body>
</html>
"""


@app.route("/")
def home():
    return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if not re.fullmatch(r"[a-z0-9_]{3,30}", username):
            error = "用户名需要是 3—30 位英文字母、数字或下划线。"
        elif not 12 <= len(password) <= 128:
            error = "密码长度需要在 12—128 个字符之间。"
        else:
            try:
                with closing(sqlite3.connect(database)) as db:
                    db.execute(
                        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
                    )
                    db.commit()
            except sqlite3.IntegrityError:
                error = "这个用户名已经注册，请换一个。"
            else:
                flash("注册成功！账号已经保存在本机。")
                return redirect(url_for("register"))
    return render_template_string(REGISTER_PAGE, error=error)


@app.errorhandler(CSRFError)
def csrf_error(error):
    return '表单已失效，请<a href="/register">重新打开注册页面</a>后再提交。', 400


from auth import auth_bp

app.register_blueprint(auth_bp)
app.config["PERMANENT_SESSION_LIFETIME"] = 1800


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)