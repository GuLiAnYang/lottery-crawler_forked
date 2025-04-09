# python-Crawler
简单了解怎么爬取足球联赛赛程赛果,并保存到excle表里

## 安装依赖
  1.安装requests库,pandas库
  ```bash
  pip install requests
  pip install pandas
  ```

## 快速开始
  1.找到想要爬取的网页的url
  2.使用requests.get获取网页内容
  ```bash
  import requests,json,csv
  import pandas as pd
  url = "这里填要爬取的网页的url"
  response = requests.get(url=url)#获取网页内容
  ```
  [![例子](https://webapi.sporttery.cn/gateway/uniform/football/league/getMatchResultV1.qry?seasonId=11817&uniformLeagueId=72&startDate=2025-04-05&endDate=2025-04-11))
