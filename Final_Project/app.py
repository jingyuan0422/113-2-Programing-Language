import pandas as pd
import streamlit as st
import asyncio
import plotly.express as px
from utils.pdf_reader import extract_text_from_pdf
from utils.resume_analyzer import run_analysis
from utils.keyword_matcher import clean_and_tokenize, classify_jd_keywords, compute_overlap
from utils.visualize_result import visualize_result
from utils.comprehensive_suggestion import generate_suggestion

# 顯示平台標題
st.title("🔍 ResuAI 智慧履歷分析平台")

# --- 🔺 履歷上傳區（全域共用） ---
st.markdown("## 📤 上傳履歷 PDF")
uploaded_file = st.file_uploader("請上傳您的履歷 PDF 檔案", type=["pdf"], key="resume_upload")

# 初始化 Session State
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "jd_input" not in st.session_state:
    st.session_state.jd_input = ""
if "result_dict" not in st.session_state:
    st.session_state.result_dict = None
if "cluster_analysis" not in st.session_state:
    st.session_state.cluster_analysis = None
if "df_experience" not in st.session_state:
    st.session_state.df_experience = None
if "fig" not in st.session_state:
    st.session_state.fig = None

# 處理履歷上傳
if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.session_state.resume_text = resume_text
    st.success("履歷上傳成功 ✅")

    with st.expander("📄 點我查看履歷文字內容"):
        st.text(resume_text)
else:
    st.info("請先上傳履歷，才能使用下方功能")

# --- 分頁：JD 關鍵字分析 & 履歷屬性分析 ---
tab1, tab2, tab3 = st.tabs(["🧩 職缺關鍵字分析", "📂 履歷屬性分析", "📘 綜合建議報告"])

# --- 🧩 JD 關鍵字分析 ---
with tab1:
    st.subheader("🧩 JD 關鍵字匹配分析")
    jd_input = st.text_area("請貼上職缺描述（Job Description）：", height=200, key="jd_input")

    if st.button("進行關鍵字分析"):
        if st.session_state.resume_text and jd_input:

            async def run_keyword_analysis():
                result = await compute_overlap(
                    st.session_state.resume_text, jd_input, classify_jd_keywords
                )
                result_dict = {
                    "與職缺的匹配程度": f"{result['match_score']} 分",
                    "硬實力技能分數": f"{result['hard_score']} 分",
                    "軟實力特質分數": f"{result['soft_score']} 分",
                    "建議新增的技能": [kw for kw, _ in result["top_missing_hard"]],
                    "建議新增的能力": [kw for kw, _ in result["top_missing_soft"]],
                }

                # 存進 session_state
                st.session_state["keyword_result"] = result_dict
                st.session_state.result = result
                st.session_state.result_dict = result_dict

                visualize_result(result_dict)

            asyncio.run(run_keyword_analysis())

        else:
            st.warning("請確認履歷已上傳且 JD 已填寫")

    # 如果結果已存在，就顯示出來
    elif st.session_state.result_dict:
        visualize_result(st.session_state.result_dict)

# --- 📂 履歷屬性分析 ---
with tab2:
    st.subheader("📂 履歷屬性分析")

    if st.session_state.resume_text:
        if st.button("執行履歷屬性分析"):
            async def run_analysis_job():
                df_experience, fig, cluster_analysis = await run_analysis(st.session_state.resume_text)

                # 存入 session_state
                st.session_state["resume_result"] = cluster_analysis
                st.session_state.df_experience = df_experience
                st.session_state.fig = fig
                st.session_state.cluster_analysis = cluster_analysis

                st.write("📊 屬性分析結果：")
                st.dataframe(df_experience)
                st.plotly_chart(fig)
                st.markdown("### 📌 屬性分析說明")
                st.markdown(cluster_analysis)

            asyncio.run(run_analysis_job())

        # 如果已經分析過，直接顯示
        elif st.session_state.df_experience is not None:
            st.write("📊 屬性分析結果：")
            st.dataframe(st.session_state.df_experience)
            st.plotly_chart(st.session_state.fig)
            st.markdown("### 📌 屬性分析說明")
            st.markdown(st.session_state.cluster_analysis)

    else:
        st.warning("請先上傳履歷才能進行分析")

# --- 📘 綜合建議報告 ---
with tab3:
    st.subheader("📘 綜合建議報告")

    if st.session_state.get("resume_text") and st.session_state.get("keyword_result") and st.session_state.get("resume_result"):
        if st.button("產生綜合建議報告"):
            with st.spinner("正在產生建議報告...請稍候"):
                async def run_comprehensive():
                    report = await generate_suggestion(
                        keyword_result=st.session_state["keyword_result"],
                        resume_result=st.session_state["resume_result"]
                    )
                    st.session_state["comprehensive_suggestion"] = report
                    st.markdown(report)
                asyncio.run(run_comprehensive())
    else:
        st.warning("請先完成 JD 關鍵字分析與履歷屬性分析，才能產生綜合建議報告。")