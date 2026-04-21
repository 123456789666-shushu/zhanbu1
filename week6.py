import streamlit as st
import math
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# 初始化会话状态
if 'best_match' not in st.session_state:
    st.session_state.best_match = ""
if 'distances' not in st.session_state:
    st.session_state.distances = {}
if 'answer' not in st.session_state:
    st.session_state.answer = None
if 'weilai' not in st.session_state:
    st.session_state.weilai = ""

# 设置页面标题和说明
st.title("🔮 亲密关系占卜")
st.caption("本项目由鼠鼠开发，绿色无广，概不收费~")

# 分割线：用户信息输入区域
st.divider()

# 获取用户输入
name = st.text_input("请输入你的代号：")

# 确认用户知情
if st.checkbox("占卜结果并不完全科学，我已知情"):
    st.success("好的呢，请开始神秘的占卜之旅吧~")
else:
    st.error("请先勾选再开始占卜！")

# 分割线：第一组问题
st.divider()

# 第一组问题：社交伙伴维度
st.caption("请根据你与对方的实际互动情况，选择最符合的分数")
a = st.radio("1.我和他/她主要在特定的场合或活动中互动（如工作、学习、运动），很少在其他情境见面。", [0, 2, 4, 6, 8, 10])
b = st.radio("2.我们的交流内容大多围绕具体事务（如任务进度、学习问题、活动安排），很少涉及个人情感。", [0, 2, 4, 6, 8, 10])
c = st.radio("3.如果离开当前共同的环境（如换工作、毕业），我们很可能不再保持密切联系。", [0, 2, 4, 6, 8, 10])
d = st.radio("4.我需要他/她帮忙时，通常会限于与共同活动相关的事情（如借笔记、协调工作）。", [0, 2, 4, 6, 8, 10])
e = st.radio("5.我对他/她的了解主要停留在表面（如兴趣爱好、专业能力），并不清楚其内心深处的脆弱或秘密。", [0, 2, 4, 6, 8, 10])

# 分割线：第二组问题
st.divider()

# 第二组问题：依恋对象维度
st.caption("请根据你对对方的情感依赖程度，选择最符合的分数")
f = st.select_slider("6.当我感到焦虑、害怕或难过时，我首先会想联系他/她寻求安慰。", options=[0, 2, 4, 6, 8, 10])
g = st.select_slider("7.有他/她在身边，我会觉得更有安全感，能够更放心地去探索新事物或面对挑战。", options=[0, 2, 4, 6, 8, 10])
h = st.select_slider("8.即使我们暂时分开，我也坚信他/她会在我需要时及时回应我。", options=[0, 2, 4, 6, 8, 10])
i = st.select_slider("9.我会在他/她面前表现出脆弱、哭泣或依赖的一面，而不担心被嫌弃。", options=[0, 2, 4, 6, 8, 10])
j = st.select_slider("10.他/她的认可和鼓励对我情绪的影响非常大，失去他/她的支持会让我感到不安。", options=[0, 2, 4, 6, 8, 10])

# 分割线：第三组问题
st.divider()

# 第三组问题：灵魂伴侣维度
st.caption("请根据你与对方的精神契合度，填写最符合的分数")
k = st.number_input("11.我感觉我们之间有一种超越言语的默契，常常不需要解释就能理解彼此的想法。", min_value=0, max_value=10, step=2)
l = st.number_input("12.与他/她相处时，我可以完全真实地做自己，没有任何需要伪装的部分。", min_value=0, max_value=10, step=2)
m = st.number_input("13.我相信我们的相遇或关系带有某种“命中注定”的意义，不是偶然的。", min_value=0, max_value=10, step=2)
n = st.number_input("14.即使发生激烈的冲突，我也确信我们最终会和解，并且关系会因此更深。", min_value=0, max_value=10, step=2)
o = st.number_input("15.我能够接受他/她所有的不完美，同时他/她也能接纳我所有的阴暗面。", min_value=0, max_value=10, step=2)

# 分割线：占卜结果区域
st.divider()

# 计算各维度得分
score_1 = a + b + c + d + e  # 社交伙伴维度得分
score_2 = f + g + h + i + j  # 依恋对象维度得分
score_3 = k + l + m + n + o  # 灵魂伴侣维度得分
user = [score_1, score_2, score_3]  # 用户得分向量

# 定义三种关系类型的标准向量
profiles = {
    "社交伙伴": [10, 3, 3],
    "依恋对象": [3, 10, 3],
    "灵魂伴侣": [3, 3, 10]
}

# 初始化变量
min_dist = 999999.0  # 最小距离

# 一键占卜按钮
if st.button("一键占卜", use_container_width=True):
    # 计算用户得分与各标准向量的欧氏距离
    local_distances = {}
    local_best_match = ""
    local_min_dist = 999999.0
    
    for title, coords in profiles.items():
        dist = math.sqrt((user[0] - coords[0]) ** 2 + (user[1] - coords[1]) ** 2 + (user[2] - coords[2]) ** 2)
        local_distances[title] = dist
        # 更新最小距离和最佳匹配
        if dist < local_min_dist:
            local_min_dist = dist
            local_best_match = title
    
    # 存储结果到会话状态
    st.session_state.best_match = local_best_match
    st.session_state.distances = local_distances
    
    # 显示结果
    st.balloons()  # 显示气球动画
    st.toast("占卜完成！")

# 持久显示占卜结果
if st.session_state.best_match:
    st.success(f"{name}，你们的关系极有可能是：{st.session_state.best_match} !")

# 后续问题：是否理想关系
st.session_state.answer = st.radio("该结果是你的理想关系吗？", ["是理想关系", "不是理想关系"], horizontal=True, index=None, key="answer_radio")

if st.session_state.answer == "不是理想关系":
    # 请求神秘力量抽签按钮
    if st.button("请求获得神秘力量，一键抽签", use_container_width=True):
        # 选择距离第二小的关系类型
        if st.session_state.distances:
            # 对距离按升序排序
            sorted_distances = sorted(st.session_state.distances.items(), key=lambda x: x[1])
            # 取第二个元素（距离第二小的）
            if len(sorted_distances) >= 2:
                local_weilai = sorted_distances[1][0]
            else:
                # 如果只有一个关系类型，就选它
                local_weilai = sorted_distances[0][0]
        else:
            # 如果还没有占卜，就随机选择
            list = ["社交伙伴", "依恋对象", "灵魂伴侣"]
            local_weilai = random.choice(list)
        
        # 存储结果到会话状态
        st.session_state.weilai = local_weilai
        
        # 显示进度条
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
        st.toast("抽签完成！")
    
    # 持久显示抽签结果
    if st.session_state.weilai:
        st.success(f"将来你们可能是：{st.session_state.weilai}~")
elif st.session_state.answer == "是理想关系":
    st.success(f"恭喜你噢！感谢参与~")

# 分割线：结束区域
st.divider()

# 查看科学统计按钮
if st.button("查看科学统计", use_container_width=True):
    if st.session_state.distances:  # 确保已经进行了占卜
        # 使用pandas绘制距离图表
        st.subheader("各关系类型匹配度")
        df = pd.DataFrame(list(st.session_state.distances.items()), columns=["关系类型", "距离"])
        # 距离越小，匹配度越高，所以转换为匹配度百分比
        df["匹配度"] = (1 - df["距离"] / df["距离"].max()) * 100
        
        # 显示数据表格
        st.dataframe(df)
        
        # 绘制柱状图
        fig, ax = plt.subplots()
        ax.bar(df["关系类型"], df["匹配度"])
        ax.set_ylabel("匹配度 (%)")
        ax.set_title("各关系类型匹配度分析")
        st.pyplot(fig)
    else:
        st.warning("请先进行一键占卜，再查看科学统计！")


