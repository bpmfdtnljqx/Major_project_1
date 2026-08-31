import json
import os
import re
import jieba
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
#设置中文字体
font_path = (
    "/usr/share/fonts/opentype/noto/"
    "NotoSansCJK-Regular.ttc"
)
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()
plt.rcParams["axes.unicode_minus"] = False
#读取歌曲数据
with open("data/raw/song.json","r",encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)
#设置停用词
stop_words = {
    # 常见虚词
    "的",
    "了",
    "我",
    "你",
    "他",
    "她",
    "它",
    "是",
    "在",
    "有",
    "和",
    "也",
    "都",
    "不",
    "就",
    "还",
    "啊",
    "吗",
    "呢",
    "吧",
    "这",
    "那",
    "一个",
    "没有",
    "自己",
    "我们",
    "你们",
    "他们",
    "欣赏",
    # 歌词元数据
    "作词",
    "作曲",
    "编曲",
    "制作",
    "制作人",
    "混音",
    "录音",
    "母带",
    "监制",
    "吉他",
    "贝斯",
    "鼓",
    "钢琴",
    "音乐",
    "编写",
    # 纯音乐提示
    "纯音乐",
    "请欣赏"
}
#将歌手名加入停用词
for artist_names in df["artist_names"].dropna():
    artists = str(artist_names).split(",")
    for artist in artists:
        artist = artist.strip()
        if artist:
            stop_words.add(artist)

#歌词分词函数
def tokenize_lyric(lyric):
    words = jieba.lcut(str(lyric))
    result = []
    for word in words:
        word = word.strip()
        # 空字符串
        if not word:
            continue
        # 停用词
        if word in stop_words:
            continue
        # 单字
        if len(word) == 1:
            continue
        # 纯数字
        if word.isdigit():
            continue
        # 纯英文
        if re.fullmatch(r"[A-Za-z]+", word):
            continue
        # 不包含中文
        if not re.search(r"[\u4e00-\u9fff]",word):
            continue
        result.append(word)
    return result

#对每首歌曲进行分词
song_words = []
for lyric in df["lyric"]:
    words = tokenize_lyric(lyric)
    song_words.append(words)
#统计所有歌曲的总词频
all_words = []
for words in song_words:
    all_words.extend(words)
word_counts = Counter(all_words)
#统计每个词覆盖的歌曲数量
word_song_count = Counter()
for words in song_words:
    #保证同一个词在同一首歌中只计算一次
    unique_words = set(words)
    for word in unique_words:
        word_song_count[word] += 1
#构造词语统计表
word_results = []
for word, frequency in word_counts.items():
    song_count = word_song_count[word]
    song_percentage = (song_count/len(df)*100)
    word_results.append({
        "word": word,
        "frequency": frequency,
        "song_count": song_count,
        "song_percentage": song_percentage
    })
word_result = pd.DataFrame(word_results)
#筛选具有一定代表性的词
analysis_result = word_result[
    word_result["frequency"] >= 20
].copy()
#计算词频与歌曲覆盖数的相关系数
correlation = (
    analysis_result["frequency"]
    .corr(
        analysis_result["song_count"]
    )
)
#保存相关系数
correlation_result = pd.DataFrame({
    "metric": [
        "Pearson correlation"
    ],
    "value": [
        correlation
    ]
})
correlation_result.to_csv("analysis/output/lyric_correlation.csv",index=False,encoding="utf-8-sig")
#绘制词频与歌曲覆盖数散点图
plt.figure(figsize=(10, 7))
plt.scatter(
    analysis_result["song_count"],
    analysis_result["frequency"]
)
plt.xlabel("歌曲覆盖数")
plt.ylabel("词频")
plt.title("歌词词频与歌曲覆盖数的关系")
#标注词频最高的10个词
top_labels = (
    analysis_result
    .sort_values("frequency",ascending=False)
    .head(10)
)
for _, row in top_labels.iterrows():
    plt.annotate(
        row["word"],
        (
            row["song_count"],
            row["frequency"]
        )
    )
plt.tight_layout()
plt.savefig("analysis/output/lyric_frequency_coverage.png",dpi=300)
plt.close()
#保存用于相关性分析的数据
analysis_result.to_csv("analysis/output/lyric_frequency_coverage.csv",index=False,encoding="utf-8-sig")
#按总词频排序
top_frequency = (
    analysis_result
    .sort_values("frequency",ascending=False)
    .head(20)
    .reset_index(drop=True)
)
#按歌曲覆盖率排序
top_coverage = (
    analysis_result
    .sort_values("song_percentage",ascending=False)
    .head(20)
    .reset_index(drop=True)
)
#创建输出目录
os.makedirs("analysis/output",exist_ok=True)
#保存Top 20词频
top_frequency.to_csv("analysis/output/lyric_top_frequency.csv",index=False,encoding="utf-8-sig")
#保存Top 20歌曲覆盖率
top_coverage.to_csv("analysis/output/lyric_top_coverage.csv",index=False,encoding="utf-8-sig")
#绘制Top 20词频
frequency_plot = (
    top_frequency
    .sort_values("frequency")
)
plt.figure(figsize=(10, 8))
plt.barh(
    frequency_plot["word"],
    frequency_plot["frequency"]
)
plt.xlabel("出现次数")
plt.ylabel("词语")
plt.title("歌词高频词 Top 20")
plt.tight_layout()
plt.savefig("analysis/output/lyric_top_frequency.png",dpi=300)
plt.close()
#绘制Top 20歌曲覆盖率
coverage_plot = (
    top_coverage
    .sort_values("song_percentage")
)
plt.figure(figsize=(10, 8))
plt.barh(
    coverage_plot["word"],
    coverage_plot["song_percentage"]
)
plt.xlabel("歌曲覆盖率（%）")
plt.ylabel("词语")
plt.title("歌词词语歌曲覆盖率 Top 20")
plt.tight_layout()
plt.savefig("analysis/output/lyric_top_coverage.png",dpi=300)
plt.close()