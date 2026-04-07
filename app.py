import streamlit as st
import pandas as pd
import numpy as np

# 页面配置
st.set_page_config(
    page_title="学生练习数据查询",
    page_icon="📊",
    layout="centered"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('data.xlsx')
        return df
    except Exception as e:
        st.error(f"数据加载失败：{e}")
        return None

# 主应用
def main():
    # 标题
    st.markdown('<h1 class="main-header">📊 学生练习数据查询系统</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 加载数据
    df = load_data()
    
    if df is None:
        st.stop()
    
    # 查询输入区域
    st.markdown("### 🔍 查询信息")
    st.markdown("请输入您的手机号或学号进行查询")
    
    # 输入框
    search_input = st.text_input(
        "手机号/学号",
        placeholder="请输入11位手机号或学号",
        max_chars=50,
        help="输入您的手机号（11位数字）或学号即可查询"
    )
    
    # 查询按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        search_button = st.button("🔍 查询", use_container_width=True, type="primary")
    
    # 执行查询
    if search_button and search_input:
        # 清理输入
        search_input = search_input.strip()
        
        # 尝试匹配手机号或用户ID
        result = None
        
        # 先尝试按手机号匹配（如果是数字）
        if search_input.isdigit():
            phone = int(search_input)
            result = df[df['手机号'] == phone]
        
        # 如果没找到，尝试按用户ID匹配
        if result is None or len(result) == 0:
            result = df[df['用户ID'].str.contains(search_input, case=False, na=False)]
        
        # 显示结果
        if len(result) > 0:
            student = result.iloc[0]
            
            # 成功提示
            st.markdown(f'<div class="success-message">✅ 查询成功！欢迎您，<strong>{student["用户昵称"]}</strong></div>', unsafe_allow_html=True)
            
            # 学生基本信息
            st.markdown("### 👤 基本信息")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**用户昵称：** {student['用户昵称']}")
                st.info(f"**用户标签：** {student['用户标签']}")
            with col2:
                st.info(f"**手机号：** {student['手机号']}")
                st.info(f"**练习次数：** {student['练习次数']} 次")
            
            st.markdown("---")
            
            # 练习时长
            st.markdown("### ⏱️ 练习时长")
            st.success(f"**累计练习时长：** {student['练习时长']}")
            
            st.markdown("---")
            
            # 成绩数据
            st.markdown("### 📈 成绩数据")
            
            # 分数展示
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="最高分数",
                    value=f"{student['最高分数']}分",
                    delta=None
                )
                # 进度条
                progress_max = student['最高分数'] / 100
                st.progress(progress_max)
            
            with col2:
                st.metric(
                    label="平均分数",
                    value=f"{student['平均分数']}分",
                    delta=None
                )
                # 进度条
                progress_avg = student['平均分数'] / 100
                st.progress(progress_avg)
            
            with col3:
                st.metric(
                    label="最低分数",
                    value=f"{student['最低分数']}分",
                    delta=None
                )
                # 进度条
                progress_min = student['最低分数'] / 100 if student['最低分数'] > 0 else 0
                st.progress(progress_min)
            
            st.markdown("---")
            
            # 成绩评价
            st.markdown("### 📝 成绩评价")
            avg_score = student['平均分数']
            
            if avg_score >= 90:
                grade = "优秀 ⭐⭐⭐⭐⭐"
                color = "green"
                suggestion = "继续保持！你是大家学习的榜样！"
            elif avg_score >= 80:
                grade = "良好 ⭐⭐⭐⭐"
                color = "blue"
                suggestion = "进步明显！再接再厉，争取更好成绩！"
            elif avg_score >= 70:
                grade = "中等 ⭐⭐⭐"
                color = "orange"
                suggestion = "基础不错！多加练习，一定会有更大提升！"
            elif avg_score >= 60:
                grade = "及格 ⭐⭐"
                color = "yellow"
                suggestion = "需要加油！多花时间练习，相信你会越来越好！"
            else:
                grade = "需努力 ⭐"
                color = "red"
                suggestion = "不要灰心！坚持练习，一定会有进步！"
            
            st.markdown(f"**等级评定：** :{color}[{grade}]")
            st.info(f"💡 {suggestion}")
            
        else:
            # 未找到记录
            st.warning("⚠️ 未找到相关记录，请检查输入是否正确")
            st.markdown("**提示：**")
            st.markdown("- 请确认输入的手机号或学号是否正确")
            st.markdown("- 如果仍有问题，请联系老师或管理员")
    
    # 页脚信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
        <p>📚 本系统仅供学生查询个人数据使用</p>
        <p>数据更新时间：2026-04-03</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
