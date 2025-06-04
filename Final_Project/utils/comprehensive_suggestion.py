# utils/comprehensive_suggestion.py

import os
from dotenv import load_dotenv
from typing import Dict
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

async def generate_suggestion(keyword_result: Dict, resume_result: str) -> str:
    """
    根據 JD 匹配結果與履歷屬性分析結果，產生綜合建議報告。
    """

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "❌ 無法讀取 GEMINI_API_KEY，請確認 .env 檔案設置正確"

    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        api_key=api_key,
    )

    prompt = f"""
    請根據以下履歷分析資料，撰寫一份完整的建議報告，格式包含：

    1. 整體優勢總結
    2. 與職缺的匹配分析
    3. 履歷呈現建議
    4. 推薦補強項目
    5. 求職策略建議

    📌 JD 匹配分析：
    {keyword_result}

    📌 履歷屬性分析：
    {resume_result}

    請用條列式清楚地說明，報告內容控制在 500 字內。
    """

    try:
        response = await model_client.create(
            messages=[UserMessage(source="user", content=prompt)]
        )
        return response.content
    except Exception as e:
        return f"❌ 產生建議失敗：{str(e)}"
