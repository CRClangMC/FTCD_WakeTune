# 14歌曲投稿系统（ftcdsauto）

一个基于 Django 的歌曲投稿与投票系统，由 FTCD studio 开发。用户可以注册投稿账号、投稿歌曲、为歌曲投票；管理员负责审核歌曲、锁榜；超级管理员负责管理用户、重置每周数据等。

> 项目版权信息：Copyright © 2024 FTCD All Rights Reserved. FTCD studio 版权所有

## 目录

- [功能概览](#功能概览)
- [环境要求](#环境要求)
- [安装与配置](#安装与配置)
- [运行项目](#运行项目)
- [页面说明](#页面说明)
  - [用户端页面](#用户端页面)
  - [管理员端页面](#管理员端页面)
- [数据库表说明](#数据库表说明)
- [短信服务配置](#短信服务配置)
- [许可证](#许可证)

## 功能概览

- 用户通过手机号 + 短信验证码注册投稿账号
- 用户登录后投稿歌曲、为已有歌曲投票
- 查看本周入围歌曲榜单
- 管理员审核（过审）歌曲、删除歌曲、锁榜
- 超级管理员管理预选列表、重置每周数据、修改用户投票/投稿次数
- 修改用户密码 / 管理员密码

## 环境要求

- Python 3.x
- Django
- pyodbc
- Microsoft Access 数据库驱动（`Microsoft Access Driver (*.mdb, *.accdb)`，用于连接业务数据库 `数据库ftcd.mdb`）
- 阿里云短信 SDK：
  - `alibabacloud_dysmsapi20170525`
  - `alibabacloud_tea_openapi`
  - `alibabacloud_tea_util`

> 项目自带一个 `db.sqlite3`（Django 框架使用的 SQLite 数据库），业务数据存放在 `数据库ftcd.mdb`（Access 数据库）中。

## 安装与配置

1. **安装依赖**

   ```bash
   pip install django pyodbc alibabacloud_dysmsapi20170525 alibabacloud_tea_openapi alibabacloud_tea_util
   ```

2. **配置 Django SECRET_KEY**

   打开 [`mylibrary/settings.py`](mylibrary/settings.py)，修改 `SECRET_KEY`：

   ```python
   SECRET_KEY = 'your-new-secret-key'
   ```

3. **配置允许访问的主机**

   在 [`mylibrary/settings.py`](mylibrary/settings.py) 中修改 `ALLOWED_HOSTS`，例如：

   ```python
   ALLOWED_HOSTS = ['*']  # 生产环境建议填写具体域名或 IP
   ```

4. **配置数据库**

   - Django 默认使用根目录下的 `db.sqlite3`。
   - 业务数据库为根目录下的 `数据库ftcd.mdb`（Access），代码通过 ODBC 连接，确保系统已安装 Microsoft Access 驱动且文件路径正确。

5. **配置阿里云短信服务（重要）**

   短信 AccessKey 不再硬编码在代码中，改为通过环境变量读取。请设置以下两个环境变量：

   ```bash
   # Windows (PowerShell)
   $env:ALIYUN_ACCESS_KEY_ID = "your-access-key-id"
   $env:ALIYUN_ACCESS_KEY_SECRET = "your-access-key-secret"

   # Linux / macOS
   export ALIYUN_ACCESS_KEY_ID="your-access-key-id"
   export ALIYUN_ACCESS_KEY_SECRET="your-access-key-secret"
   ```

   短信签名和模板代码在 [`show/views.py`](show/views.py) 的 `Sample` 类中配置：

   ```python
   send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
       sign_name='FTCD工作室',        # 短信签名
       template_code='SMS_472415118', # 短信模板代码
       ...
   )
   ```

6. **收集静态文件（生产环境）**

   ```bash
   python manage.py collectstatic
   ```

   或双击运行 [`收集静态文件.bat`](收集静态文件.bat)。

## 运行项目

```bash
python manage.py runserver 0.0.0.0:8000
```

或双击运行 [`运行python程序.bat`](运行python程序.bat)。浏览器访问 `http://127.0.0.1:8000/`。

## 页面说明

### 用户端页面

| URL | 视图函数 | 模板 | 作用 |
| --- | --- | --- | --- |
| `/` | `login` | [`login.html`](show/templates/login.html) | 投稿账号登录页。输入用户名和密码登录，登录成功后跳转到 `/musictg/`。 |
| `/login/` | `login` | [`login.html`](show/templates/login.html) | 同上，登录页的带名称路由。 |
| `/accessph/` | `accessph` | [`accessph.html`](show/templates/accessph.html) | 注册第一步：输入手机号，点击"获取验证码"后系统调用阿里云短信接口发送 6 位随机验证码。已注册的手机号会提示"此手机号已注册"。 |
| `/accessph2/` | `accessph2` | [`accessph2.html`](show/templates/accessph2.html) | 注册第二步：输入收到的短信验证码进行校验。校验通过后进入设置用户名密码；点击"重新填写手机号"可返回上一步。 |
| `/access/` | `access` | [`access.html`](show/templates/access.html) | 注册第三步：设置用户名和密码（两次密码一致）。注册成功即自动登录并跳转到 `/musictg/`。 |
| `/musictg/` | `musictg` | [`musictg.html`](show/templates/musictg.html) | 用户主页：显示歌曲列表（歌名、歌手、票数、试听链接），支持投稿（需有投稿次数）、投票（需有投票次数）、刷新列表。 |
| `/pwdset/` | `pwdset` | [`pwdset.html`](show/templates/pwdset.html) | 修改投稿账号密码。修改成功后需重新登录。 |
| `/phblock/` | `phblock` | [`phblock.html`](show/templates/phblock.html) | 本周入围歌曲榜单页，展示已通过审核并上榜的歌曲。 |

### 管理员端页面

| URL | 视图函数 | 模板 | 作用 |
| --- | --- | --- | --- |
| `/admlogin/` | `admlogin` | [`admlogin.html`](show/templates/admlogin.html) | 管理员登录页。管理员账号存储在 `adminset` 表，登录成功跳转到 `/adminset/`。 |
| `/adminset/` | `adminset` | [`adminset.html`](show/templates/adminset.html) | 管理员操作界面：按歌名搜索、过审（把票数前 6 的歌曲写入预选列表 `yxlist`）、删除歌曲、锁榜、刷新列表。 |
| `/pwdset1/` | `pwdset1` | [`pwdset1.html`](show/templates/pwdset1.html) | 修改管理员账号密码。 |
| `/admins/` | `admins` | [`admins.html`](show/templates/admins.html) | 超级管理员登录页。超级管理员账号存储在 `adminall` 表，登录成功跳转到 `/adminall/`。 |
| `/adminall/` | `adminall` | [`adminall.html`](show/templates/adminall.html) | 超级管理员界面：查看预选列表（`yxlist`）、通过/清空预选列表、重置（恢复用户投票 4 次、投稿 1 次并清空预选列表）、解锁、删除投票前 6 的歌曲、按歌名搜索、更改歌曲票数、删除歌曲、按手机号搜索用户、更改用户投票/投稿次数等。 |

## 数据库表说明

业务数据存放在根目录的 `数据库ftcd.mdb`（Access 数据库），主要表如下：

| 表名 | 字段（依据代码推断） | 用途 |
| --- | --- | --- |
| `users` | 用户名、密码、投票次数、投稿次数、手机号 | 投稿用户账号信息 |
| `musictg` | 歌名、歌手、投票 | 用户投稿的歌曲及其票数 |
| `yxlist` | 歌名、歌手、投票 | 管理员过审后的预选列表 |
| `phblock` | 歌名、歌手、投票 | 最终入围歌曲榜 |
| `command` | 操作、用户、时间、信息、操作歌曲、操作信息 | 操作日志 |
| `adminset` | 用户名、密码 | 管理员账号 |
| `adminall` | 用户名、密码 | 超级管理员账号 |

## 短信服务配置

系统使用阿里云短信服务（Dysmsapi）发送注册验证码：

- **Endpoint**：`dysmsapi.aliyuncs.com`（在 [`show/views.py`](show/views.py) 的 `Sample.create_client()` 中配置）
- **AccessKey**：通过环境变量 `ALIYUN_ACCESS_KEY_ID`、`ALIYUN_ACCESS_KEY_SECRET` 提供
- **短信签名**：`FTCD工作室`
- **模板代码**：`SMS_472415118`
- **验证码**：`accessph` 视图中生成的 6 位随机数，通过模板参数 `{"code":"..."}` 下发

## 许可证

本项目使用 [MIT License](LICENSE)。
