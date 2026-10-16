from contextlib import closing
from pathlib import Path
import sqlite3

from flask import (
    Blueprint, current_app, flash, redirect,
    render_template_string, request, session, url_for,
)
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

PAGE = """
<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>我的账号</title>
<body style="max-width:420px;margin:60px auto;padding:20px;font-family:sans-serif">
{% for message in get_flashed_messages() %}<p>{{ message }}</p>{% endfor %}
{% if username %}
    <h1>登录成功！</h1>
    <p>欢迎你，{{ username }}。</p>
    <form method="post" action="{{ url_for('auth.logout') }}">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <button type="submit">退出登录</button>
    </form>
{% else %}
    <h1>登录账号</h1>
    {% if error %}<p role="alert">{{ error }}</p>{% endif %}
    <form method="post" action="{{ url_for('auth.login') }}">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <p><label>用户名<br><input name="username" required
            maxlength="30" autocomplete="username"></label></p>
        <p><label>密码<br><input name="password" type="password" required
            maxlength="128" autocomplete="current-password"></label></p>
        <button type="submit">登录</button>
    </form>
    <p><a href="{{ url_for('register') }}">还没有账号？去注册</a></p>
{% endif %}
</body>
</html>
"""


def database_path():
    return Path(current_app.instance_path) / "users.db"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = None
        if 3 <= len(username) <= 30 and 12 <= len(password) <= 128:
            with closing(sqlite3.connect(database_path())) as db:
                db.row_factory = sqlite3.Row
                user = db.execute(
                    "SELECT id, password_hash FROM users WHERE username = ?",
                    (username,),
                ).fetchone()
        if user is not None and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session.permanent = True
            return redirect(url_for("auth.dashboard"))
        error = "用户名或密码不正确。"
    return render_template_string(PAGE, username=None, error=error)


@auth_bp.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("auth.login"))
    with closing(sqlite3.connect(database_path())) as db:
        user = db.execute(
            "SELECT username FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))
    return render_template_string(PAGE, username=user[0], error=None)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("你已退出登录。")
    return redirect(url_for("auth.login"))


@auth_bp.after_request
def prevent_cache(response):
    response.headers["Cache-Control"] = "no-store"
    return response