import requests,json,csv
import pandas as pd
url = "https://webapi.sporttery.cn/gateway/uniform/football/league/getTablesV2.qry?seasonId=11817&uniformLeagueId=72"
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}

response = requests.get(url=url,headers=headers)
response.encoding = response.apparent_encoding

a=response.text
c=json.loads(a)
print(c)
c = c['value']['totalTables'][0]["groups"][0]["tables"]
print(c)
columns = []
for d in c[0].keys():
    columns.append(d)

dp = {}
for i in columns:
    e = []
    for j in c:
        e.append(j[i])
    dp[i] = e
print(dp)
# 将数据转换为 DataFrame
df = pd.DataFrame(dp, index=range(0,20))

# 写入 CSV 文件，第一行是列名
df.to_csv('zl2.csv',encoding="utf-16",sep="\t",index=False,mode="a")