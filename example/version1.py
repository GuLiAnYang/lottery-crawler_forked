import requests,json,csv
import pandas as pd

hot_id = []#热门联赛名字
l_ans = 0 #联赛id所属位置
s_ans = 0 #赛季id所属位置
season = [] #对应赛季列表
season_id = []#对应赛季id
league_id = [] #各联赛id
xx = 0 #榜单id
ls = {} #榜单表
urlj = "https://webapi.sporttery.cn/gateway/uniform/football/league/getTablesV2.qry?seasonId={}&uniformLeagueId={}"
urlx = "https://webapi.sporttery.cn/gateway/uniform/football/league/getMatchResultV1.qry?seasonId={}&uniformLeagueId={}&startDate={}&endDate={}"
qurl = "https://webapi.sporttery.cn/gateway/uniform/football/league/getLeagueListV1.qry"
ls[1] = urlj
ls[0] = urlx
print("请问要查询那个榜单:0->赛季榜,1->积分榜")
xx = int(input())
response = requests.get(qurl)
a=response.text
c=json.loads(a)
#获取热门榜单
hot = c["value"]["hot"]
print(hot)
for i in hot:
   hot_id.append(i["leagueAbbCnName"])
   league_id.append(i["uniformLeagueId"])
print("当前热门榜单:",*hot_id,*league_id)
print("请输入要查找的联赛名:")
name = input()
for i in range(len(hot_id)):
    if name == hot_id[i]:
        l_ans = i
for i in hot[l_ans]["seasonList"]:
    season.append(i["seasonName"])
    season_id.append(i["seasonId"])
print("当前可查询赛季名:",*season)#,*season_id
print("请输入要查询的赛季")
el_season = input()
for i in range(len(season_id)):
    if el_season == season[i]:
        s_ans = i
lid = league_id[l_ans] #联赛id
sid = season_id[s_ans] #赛季id
print(lid,sid)
if xx == 0:
    print("实例格式2025-03-01")
    print("请输入起始日期:")
    st = input()
    print("请输入结束日期:")
    end = input()
    url = ls[xx].format(sid, lid, st, end)
if xx == 1:
    url = ls[xx].format(sid, lid)
print(url)
response = requests.get(url=url)

a=response.text
c=json.loads(a)
print(c)
columns = []
if xx == 0:
    c = c['value']['matchList']
    print(c)
    time = []
    for i in c:
        time.append(i['matchDate'])
    print("获取的时间列表", time)
    for d in c[0]["subMatchList"][0].keys():
        columns.append(d)
    print("获取的标签列表",columns)
    name_score = ["sectionsNo999","sectionsNo1"]
    dp = {}
    for n in range(0,len(time)):
        for i in columns:
            e = []
            if i in name_score:
                for j in c[n]["subMatchList"]:
                    e.append(j[i][0]+"~"+j[i][2])
            else:
                for j in c[n]["subMatchList"]:
                    e.append(j[i])
            dp[i] = e
        dp['start_time'] = [time[n] for _ in range(len(e))]
        dp["leagueName"] = [name for _ in range(len(e))]
        print(dp)
        # 将数据转换为 DataFrame
        df = pd.DataFrame(dp, index=range(0,len(dp["matchTime"])))
        df.to_csv('zl2.csv', encoding="utf-16", sep="\t", index=False, mode="a")
else:
    c = c['value']['totalTables'][0]["groups"][0]["tables"]
    print(c)
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
    df = pd.DataFrame(dp, index=range(0, 20))

    df.to_csv('zl1.csv',encoding="utf-16",sep="\t",index=False,mode="a")