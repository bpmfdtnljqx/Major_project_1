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
    # 纯音乐提示
    "纯音乐",
    "请欣赏"
}
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
#按总词频排序
top_frequency = (
    word_result
    .sort_values(
        "frequency",
        ascending=False
    )
    .head(20)
    .reset_index(drop=True)
)
#按歌曲覆盖率排序
top_coverage = (
    word_result
    .sort_values(
        "song_percentage",
        ascending=False
    )
    .head(20)
    .reset_index(drop=True)
)
#创建输出目录并保存数据
os.makedirs("analysis/output",exist_ok=True)
top_frequency.to_csv("analysis/output/lyric_top_frequency.csv",index=False,encoding="utf-8-sig")
top_coverage.to_csv("analysis/output/lyric_top_coverage.csv",index=False,encoding="utf-8-sig")
#绘制图
frequency_plot = top_frequency.sort_values("frequency")
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
coverage_plot = top_coverage.sort_values("song_percentage")
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