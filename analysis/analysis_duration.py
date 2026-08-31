import json
import os
import pandas as pd
import matplotlib.pyplot as plt
#读取歌曲数据
with open("data/raw/song.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)
#判断是否为纯音乐
df["is_instrumental"] = df["lyric"].str.contains("纯音乐", na=False)
#转换歌曲时长
#转换时间
df["duration_min"] = (df["duration"]/1000/60)
#将true/false转换成歌曲类型
df["song_type"] = df["is_instrumental"].map({
    False: "Normal Songs",
    True: "Instrumental Songs"
})
#统计两类歌曲数量和比例
type_counts = df["song_type"].value_counts()
type_result = pd.DataFrame({
    "song_type": type_counts.index,
    "song_count": type_counts.values
})
type_result["percentage"] = (
    type_result["song_count"]
    / len(df)
    * 100
)
#统计歌曲时长
duration_statistics = (
    df.groupby("song_type")["duration_min"]
    .agg([
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max"
    ])
    .reset_index()
)
duration_statistics.columns = [
    "song_type",
    "song_count",
    "mean_duration",
    "median_duration",
    "std_duration",
    "min_duration",
    "max_duration"
]
#统计长歌曲比例
long_results = []
for limit in [5, 10, 15]:
    ratio = (
        df.groupby("song_type")["duration_min"]
        .apply(
            lambda x: (x > limit).mean() * 100
        )
    )
    for song_type, percentage in ratio.items():
        long_results.append({
            "duration_limit": limit,
            "song_type": song_type,
            "percentage": percentage
        })
long_ratio = pd.DataFrame(long_results)
# 创建输出目录并保存结果
os.makedirs("analysis/output",exist_ok=True)
type_result.to_csv("analysis/output/song_type_statistics.csv",index=False,encoding="utf-8-sig")
duration_statistics.to_csv("analysis/output/duration_statistics.csv",index=False,encoding="utf-8-sig")
long_ratio.to_csv("analysis/output/duration_long_ratio.csv",index=False,encoding="utf-8-sig")
#绘制时长分布直方图
plt.figure(figsize=(10, 6))
plt.hist(
    df.loc[
        df["song_type"] == "Normal Songs",
        "duration_min"
    ],
    bins=40,
    alpha=0.7,
    label="Normal Songs"
)
plt.hist(
    df.loc[
        df["song_type"] == "Instrumental Songs",
        "duration_min"
    ],
    bins=40,
    alpha=0.7,
    label="Instrumental Songs"
)
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Songs")
plt.title("Duration Distribution of Different Song Types")
plt.legend()
plt.tight_layout()
plt.savefig("analysis/output/duration_distribution.png",dpi=300)
plt.close()
#绘制箱线图
normal_duration = df.loc[
    df["song_type"] == "Normal Songs",
    "duration_min"
]
instrumental_duration = df.loc[
    df["song_type"] == "Instrumental Songs",
    "duration_min"
]
plt.figure(figsize=(8, 6))
plt.boxplot(
    [
        normal_duration,
        instrumental_duration
    ],
    tick_labels=[
        "Normal Songs",
        "Instrumental Songs"
    ]
)
plt.ylabel("Duration (minutes)")
plt.title("Duration Comparison of Different Song Types")
plt.tight_layout()
plt.savefig("analysis/output/duration_compare.png",dpi=300)
plt.close()