import csv
import json
from datetime import datetime

# 手动定义列名
CSV_HEADER = [
    "awayAbbCnName", "gameweek", "gmMatchId", "groupId", "groupName",
    "homeAbbCnName", "matchDate", "matchTime", "phaseId", "phaseName",
    "sectionsNo1", "sectionsNo999", "uniformAwayTeamId", "uniformHomeTeamId",
    "uniformMatchId", "wbsjMatchId", "wbsjMatchSc", "wbsjMatchScDesc", "start_time"
]
def csv_to_json(csv_file_path, json_file_path):
    matches = []
    encodings_to_try = ['utf-16', 'utf-8-sig', 'gb18030',  'latin1']

    for encoding in encodings_to_try:
        try:
            with open(csv_file_path, mode='r', encoding=encoding) as csv_file:
                # 跳过所有标题行（以awayAbbCnName开头）
                rows = []
                for row in csv_file:
                    stripped_row = row.lstrip('\ufeff').strip()  # 处理BOM和空白
                    if stripped_row.startswith('awayAbbCnName'):
                        continue  # 跳过标题行
                    rows.append(row)

                # 使用手动定义的列名创建DictReader
                csv_reader = csv.DictReader(
                    rows,
                    fieldnames=CSV_HEADER,
                    delimiter='\t'
                )

                # 跳过可能的残留标题行
                next(csv_reader, None)  # 跳过第一行（可能是残留标题）

                for row in csv_reader:
                    # 提取必要字段
                    match_date = datetime.strptime(
                        row['matchDate'], "%Y-%m-%d"
                    ).strftime("%Y-%m-%d")
                    match_key = f"英超_{row['homeAbbCnName']}_vs_{row['awayAbbCnName']}_{match_date}"

                    content = (
                        f"{row['homeAbbCnName']}主场迎战{row['awayAbbCnName']}。"
                        f"比赛时间：{row['matchTime']}，最终比分：{row['sectionsNo999']}。"
                    )

                    matches.append({
                        "matchKey": match_key,
                        "league": "英超",
                        "homeTeam": row['homeAbbCnName'],
                        "awayTeam": row['awayAbbCnName'],
                        "content": content
                    })
                break  # 成功读取后退出循环
        except (UnicodeDecodeError, KeyError) as e:
            print(f"尝试编码 {encoding} 失败: {str(e)}")
            continue

    if not matches:
        raise ValueError("未能成功解析CSV文件，请检查：\n1. 文件路径\n2. 实际分隔符\n3. 文件内容格式")

    # 导出JSON
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(matches, json_file, ensure_ascii=False, indent=2)


# 调用示例
csv_to_json('zl1.csv', 'output.json')