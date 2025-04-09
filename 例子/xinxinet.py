import requests,json,csv
import pandas as pd
url = "https://webapi.sporttery.cn/gateway/uniform/football/league/getMatchResultV1.qry?seasonId=11817&uniformLeagueId=72&startDate=2025-03-01&endDate=2025-04-07"
response = requests.get(url=url)

a=response.text
c=json.loads(a)
print(c)
c = c['value']['matchList']
print(c)
time = []
for i in c:
    time.append(i['matchDate'])
print("获取的时间列表",time)
columns = []
for d in c[0]["subMatchList"][0].keys():
    columns.append(d)
                                                                #开发数据选择
print("获取的标签列表",columns)

dp = {}
for n in range(0,len(time)):
    print(n)
    for i in columns:
        e = []
        for j in c[n]["subMatchList"]:
            e.append(j[i])
        dp[i] = e
    dp['start_time'] = [time[n] for _ in range(len(e))]
    print(dp)
    # 将数据转换为 DataFrame
    df = pd.DataFrame(dp, index=range(0,len(dp["matchTime"])))
    df.to_csv('zl1.csv',encoding="utf-16",sep="\t",index=False,mode="a")