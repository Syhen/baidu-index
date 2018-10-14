# baidu_index
crawl baidu index without selenium&amp;phantomjs

# requirements
- flask
- pillow
- numpy
- requests
- lxml
- docker

# install

1. 启动 `docker` 
```bash
sudo docker pull scrapinghub/splash
sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
```

2. 拷贝项目
```bash
git clone https://github.com/Syhen/baidu-index.git
``` 

3. 设置 `baidu-index` 环境变量

4. 启动flask微服务
```bash
cd baidu-index/baidu_index/backend
python index.py
```

5. 配置nginx
配置微服务的nginx，因为splash不能解析localhost

然后将 `baidu_index.core.index.get_res2` 中的域名调整为配置好的域名

6. demo
```python
from __future__ import unicode_literals

from requests.cookies import RequestsCookieJar

from baidu_index.core.index import BaiduIndexCrawler

cookies = RequestsCookieJar()
# update cookies with login
baidu_index_crawler = BaiduIndexCrawler('机器学习', cookies, start_date="2017-01-01", end_date="2017-01-31")
baidu_index_crawler.next()
# 936
```

# warning!!
禁止商用！
