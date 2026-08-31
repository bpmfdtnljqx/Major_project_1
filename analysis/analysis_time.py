import json
import os
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
year_result = pd.DataFrame({
    "publish_year": year_counts.index,
    "song_count": year_counts.values
})
#统计每个年代的歌曲数量
df["decade"] = (df["publish_year"]//10)*10
decade_counts = df["decade"].value_counts().sort_index()
decade_result = pd.DataFrame({
    "decade": decade_counts.index,
    "song_count": decade_counts.values
})
#创建输出目录并保存数据
os.makedirs("analysis/output",exist_ok=True)
year_result.to_csv("analysis/output/publish_year.csv",index=False,encoding="utf-8-sig")
decade_result.to_csv("analysis/output/publish_decade.csv",index=False,encoding="utf-8-sig")
#绘制年份图
plt.figure(figsize=(12,6))
plt.bar( year_result["publish_year"],year_result["song_count"])
plt.xlabel("publish year")
plt.ylabel("number of songs")
plt.title("distribution of songs by publish year")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("analysis/output/publish_year_distribution.png",dpi=300)
plt.close()
#根据年代绘制图
plt.figure(figsize=(10, 6))
plt.bar( decade_result["decade"].astype(str),decade_result["song_count"])
plt.xlabel("decade")
plt.ylabel("number of songs")
plt.title("distribution of songs by decade")
plt.tight_layout()
plt.savefig("analysis/output/publish_decade.png",dpi=300)
plt.close()
