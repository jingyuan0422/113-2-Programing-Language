import jieba
import string
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import re
import os
import json
import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 停用詞
stop_words = set([
    "的", "了", "和", "是", "我", "也", "就", "在", "有", "不", "與", "及", "並", "及其",
    "以及", "其", "之一", "中", "為", "你", "他", "她", "我們", "能", "這些", "並具備",
    "應用", "運行", "設定", "安裝", "文件", "品質"
])

load_dotenv()


def clean_and_tokenize(text, stopwords=stop_words):
    """
    將輸入文本進行清理與斷詞
    1. 去除標點符號
    2. 使用 jieba 進行中文斷詞
    3. 移除停用詞與空白詞
    """
    # 去除標點符號
    text = text.translate(str.maketrans('', '', string.punctuation + "、，。！？；：（）【】「」《》"))

    # 使用 jieba 中文斷詞
    tokens = jieba.lcut(text)

    # 過濾停用詞與空白
    tokens = [t for t in tokens if t.strip() and t not in stopwords]

    return tokens

async def classify_jd_keywords(tokens):
    """
    使用 Gemini 2.0 模型將詞彙清單分類為「硬實力技能」與「軟實力特質」兩類。
    回傳兩個 list，分別是硬實力技能與軟實力特質。
    """
    api_key = os.getenv('GEMINI_API_KEY')
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        api_key=api_key,
    )

    # 建立提示詞，要求回傳 JSON 格式
    prompt = f"""
    我有一份職缺詞彙清單，請幫我為這些詞分類為以下三類之一：
    1. 硬實力技能（如工具、語言、技術、方法等等，不要提取動詞）
    2. 軟實力特質（如抗壓性、溝通能力、團隊合作等等工作所需的軟實力）
    3. 其他（非職能關鍵詞）

    請以 JSON 格式輸出，例如：
    {{"Python": "硬實力技能", "溝通": "軟實力特質", "歡迎": "其他"}}

    詞彙清單如下：
    {tokens}
    """

    try:
        response = await model_client.create(
            messages=[UserMessage(source="user", content=prompt)]
        )

        # 清理模型輸出，去除 markdown ```json 標記
        content = response.content.strip()
        content = re.sub(r"^```json|```$", "", content).strip()

        # 解析 JSON
        all_classified = json.loads(content)

        # 改為 list 形式
        hard_skills = []
        soft_skills = []

        for word, label in all_classified.items():
            if label == "硬實力技能":
                hard_skills.append(word)
            elif label == "軟實力特質":
                soft_skills.append(word)

        return hard_skills, soft_skills

    except Exception as e:
        print("分類失敗：", e)
        return [], []

async def compute_overlap(resume_text, jd_text, classify_jd_keywords_func, top_n=10):
    resume_tokens = clean_and_tokenize(resume_text)
    jd_tokens = clean_and_tokenize(jd_text)

    resume_set = set(resume_tokens)
    jd_set = set(jd_tokens)

    # 使用 Gemini AI 對 JD 詞分類（await 非同步）
    hard_skills, soft_skills = await classify_jd_keywords_func(list(jd_set))

    # 匹配分析
    hard_overlap = [word for word in hard_skills if word in resume_set]
    soft_overlap = [word for word in soft_skills if word in resume_set]

    hard_score = int(len(hard_overlap) / len(hard_skills) * 100) if hard_skills else 0
    soft_score = int(len(soft_overlap) / len(soft_skills) * 100) if soft_skills else 0
    match_score = round((hard_score + soft_score) / 2, 1)

    jd_counts = Counter(jd_tokens)
    missing_hard_skills = {
        word: count for word, count in jd_counts.items()
        if word in hard_skills and word not in resume_set
    }
    missing_soft_skills = {
        word: count for word, count in jd_counts.items()
        if word in soft_skills and word not in resume_set
    }

    top_missing_hard = sorted(missing_hard_skills.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_missing_soft = sorted(missing_soft_skills.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return {
        "match_score": match_score,
        "hard_score": hard_score,
        "soft_score": soft_score,
        "top_missing_hard": top_missing_hard,
        "top_missing_soft": top_missing_soft,
        "jd_tokens": jd_tokens
    }


