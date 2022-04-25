# 推特爬虫
- 根据登录账户获取关注人信息，在关主人信息中爬取自定义的推特用户媒体数据

声明：本项目仅供学习和参考，非商用，欢迎大家fork

### 项目树

```
.
├── README.md
├── main
│   ├── scrapy.cfg
│   └── twitterSpider
│       ├── __init__.py
│       ├── api
│       │   ├── __init__.py
│       │   ├── login.py
│       │   └── twitter.py
│       ├── download.json   # 要下载推特昵称列表
│       ├── extractor
│       │   ├── __init__.py
│       │   ├── extractor.py
│       │   └── json_path_finder.py
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       ├── run.py
│       ├── settings.py # 配置文件
│       ├── spiders
│       │   ├── __init__.py
│       │   ├── download.py
│       │   └── twitter.py
│       ├── twitterLogin.db # 登录信息
│       └── utils
│           ├── __init__.py
│           ├── aes.py  # 账户密码本地加密
│           ├── sqlite.py
│           └── utils.py
├── requirements.txt
├── runTwitterSpider.sh
```

使用方法：

1. 安装依赖 `pip install -r requirements.txt`
2. 在`settings.py`中配置你的redis地址、推特账号、下载地址
3. 在`download.json`中配置你要下载的推特用户昵称
4. 开启reids-server
5. 直接运行`run.py`或配置`runTwitterSpider.sh`并运行

参考链接：

https://github.com/CharlesPikachu/DecryptLogin

https://github.com/kingname/JsonPathFinder