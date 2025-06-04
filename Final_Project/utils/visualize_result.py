import streamlit as st
import plotly.graph_objects as go

def visualize_result(result_dict):

    # 擷取分數，並四捨五入為整數
    match_score = round(float(result_dict["與職缺的匹配程度"].replace(" 分", "")))
    hard_score = round(float(result_dict["硬實力技能分數"].replace(" 分", "")))
    soft_score = round(float(result_dict["軟實力特質分數"].replace(" 分", "")))

    # 分左右兩欄呈現
    col1, col2 = st.columns(2)

    # === 左邊：整體匹配程度 ===
    with col1:
        st.markdown("### 🎯 整體匹配程度")

        ring_fig = go.Figure(go.Pie(
            values=[match_score, 100 - match_score],
            labels=["匹配", "未匹配"],
            hole=0.7,
            marker=dict(colors=["#FFD700", "#E0E0E0"]),
            textinfo='none',
            sort=False
        ))

        # 加入中央文字：匹配程度
        ring_fig.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            annotations=[dict(
                text=f"<b style='font-size:40px'>{match_score}%</b>",
                x=0.5, y=0.5,
                font_size=500,
                showarrow=False
            )],
            height=250
        )

        st.plotly_chart(ring_fig, use_container_width=True)

    # === 右邊：技能分析分數 ===
    with col2:
        st.markdown("### 🧠 技能分析分數")

        def skill_bar(label, score, color):
            fig = go.Figure(go.Bar(
                x=[score],
                y=[f"<b style='font-size:18px'>{label}</b>"],  # 放大字體
                orientation='h',
                marker=dict(color=color),
                text=[f"<b style='font-size:18px'>{score} 分</b>"],  # 放大分數字體
                textposition="outside",
                hoverinfo="none"
            ))
            fig.update_layout(
                xaxis=dict(range=[0, 100], showticklabels=False),
                yaxis=dict(showticklabels=True),
                height=100,
                margin=dict(l=60, r=20, t=10, b=10),
                plot_bgcolor="#fff",
                paper_bgcolor="#fff"
            )
            fig.update_traces(textfont=dict(size=18))
            st.plotly_chart(fig, use_container_width=True)

        skill_bar("💻 硬實力技能", hard_score, "#FFEAD5")
        skill_bar("🗣️ 軟實力特質", soft_score, "#FFF8DC")

    
    # ===== 建議新增技能與能力（二欄式）=====
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ 建議補強項目")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔧 技能建議")
        for skill in result_dict["建議新增的技能"]:
            st.markdown(
                f"""
                <div style='background-color:#FFEAD5; padding:10px 15px; margin-bottom:8px; border-radius:10px;'>
                    <b> {skill}</b>
                </div>
                """, unsafe_allow_html=True
            )

    with col2:
        st.markdown("#### 💡 能力建議")
        for trait in result_dict["建議新增的能力"]:
            st.markdown(
                f"""
                <div style='background-color:#FFF8DC; padding:10px 15px; margin-bottom:8px; border-radius:10px;'>
                    <b> {trait}</b>
                </div>
                """, unsafe_allow_html=True
            )
