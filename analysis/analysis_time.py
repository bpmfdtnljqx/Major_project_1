import json
import pandas as pd
import matplotlib.pyplot as plt

#读取歌手数据
with open("data/raw/song.json","r",encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)
#转换时间戳
df["publish_date"] = pd.to_datetime(df["publish_time"],unit="ms")
#从日期中提取年份
df["publish_year"] = df["publish_date"].dt.year
#统计每年歌曲数量
year_counts = df["publish_year"].value_counts().sort_index()
#绘制年份图
plt.figure(figsize=(12,6))
plt.bar(year_counts.index,year_counts.values)
plt.xlabel("publish year")
plt.ylabel("number of songs")
plt.title("distribution of songs by publish year")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("analysis/publish_year_distribution.png",dpi=300)
plt.show()
