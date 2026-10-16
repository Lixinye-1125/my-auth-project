# 我的登录认证项目

使用 Python、Flask 和 SQLite 制作的本机学习项目。

支持注册、登录、查看个人页面和退出登录。

## 文件用途

| 文件 | 用途 |
|---|---|
| app.py | 初始化应用、密钥和数据库，处理注册 |
| auth.py | 处理登录、个人页面和退出登录 |
| requirements.txt | 软件包依赖清单 |
| .gitignore | 指定 Git 忽略的本地文件 |
| instance/users.db | 本机账号数据库，自动创建 |
| instance/secret.key | 本机签名密钥，自动创建 |

## 安装与启动

在项目文件夹中打开 PowerShell，依次运行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

浏览器打开：http://127.0.0.1:5000/login

已经创建好环境时，只需运行最后一条启动命令。
在运行程序的终端中按 Ctrl+C 可以停止服务。

## 页面和接口

| 地址 | 请求方法 | 功能 |
|---|---|---|
| / | GET | 跳转到注册页面 |
| /register | GET、POST | 显示注册表单、创建账号 |
| /login | GET、POST | 显示登录表单、校验密码 |
| /dashboard | GET | 检查登录状态后显示个人页面 |
| /logout | POST | 清除当前浏览器的登录状态 |

## 认证流程

1. 注册：检查用户名和密码格式，将用户名与密码哈希保存到 SQLite。
2. 登录：查询账号，通过 check_password_hash 核对密码。
3. 核对成功：清理旧 Session，写入 user_id，跳转到个人页面。
4. 访问个人页面：检查 Session 中的 user_id，并查询用户是否存在。
5. 退出：清除 Session，跳转到登录页面。

## 密码、密钥和令牌

- 密码使用 Werkzeug 默认的 scrypt 方法生成带盐哈希，数据库不保存明文密码。
- 数据库查询使用参数绑定。
- Flask 使用签名 Cookie 保存 Session；签名用于防篡改，不是加密。
- Session 包含用户编号、CSRF 校验数据等，不保存密码。
- 登录会话设为 30 分钟，持续访问时会刷新。
- Flask-WTF 为注册、登录和退出的 POST 请求提供 CSRF 校验。
- CSRF 令牌用于验证表单提交，和登录状态用途不同。
- 本项目没有使用 JWT、OAuth 或独立的访问令牌、刷新令牌。
- 数据库和签名密钥位于 instance 文件夹，由 .gitignore 忽略。

## 当前范围

这是本机学习版，尚未配置 HTTPS、登录限流和服务端会话撤销。
退出会清除当前浏览器的会话，但不能主动撤销此前复制出去的有效 Cookie。