import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(
    page_title="学生练习数据查询",
    page_icon="📊",
    layout="centered"
)

# 加载数据
@st.cache_data
def load_data():
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data.xlsx')
    
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"数据加载失败：{e}")
        return None

# 主应用
def main():
    # 标题
    st.title("📊 学生练习数据查询系统")
    st.markdown("---")
    
    # 加载数据
    df = load_data()
    
    if df is None:
        st.error("无法加载数据文件，请联系管理员")
        return
    
    # 搜索框
    st.markdown("### 🔍 请输入查询信息")
    search_input = st.text_input(
        "输入手机号或学号（用户ID）", 
        placeholder="例如：13912345678 或 urs-phoneyd.xxx@163.com",
        label_visibility="collapsed"
    )
    
    if st.button("查询", type="primary"):
        if not search_input.strip():
            st.warning("请输入手机号或学号")
            return
        
        # 查询逻辑
        search_input = search_input.strip()
        
        # 尝试匹配手机号（数字）
        try:
            phone_search = int(search_input)
            result = df[df['手机号'] == phone_search]
        except:
            # 尝试匹配学号（字符串）
            result = df[df['用户ID'].str.contains(search_input, case=False, na=False)]
        
        if len(result) == 0:
            st.error("未找到相关信息，请检查输入是否正确")
        else:
            row = result.iloc[0]
            
            # 显示结果
            st.success(f"✅ 查询成功！")
            st.markdown("---")
            
            # 基本信息
            col1, col2 = st.columns(2)
            with col1:
                st.metric("姓名", row['用户昵称'])
                st.metric("班级", row['用户标签'])
            with col2:
                st.metric("练习次数", f"{row['练习次数']}次")
                st.metric("练习时长", row['练习时长'])
            
            st.markdown("---")
            
            # 成绩信息
            st.markdown("### 📈 成绩信息")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("最高分", f"{row['最高分数']}分")
            with col2:
                st.metric("平均分", f"{row['平均分数']}分")
            with col3:
                st.metric("最低分", f"{row['最低分数']}分")
            
            # 分数进度条
            st.markdown("### 📊 成绩可视化")
            avg_score = row['平均分数']
            st.progress(avg_score / 100)
            st.caption(f"平均分占比：{avg_score}%")
            
            # 评价
            if avg_score >= 90:
                rating = "⭐⭐⭐⭐⭐ 优秀"
            elif avg_score >= 80:
                rating = "⭐⭐⭐⭐ 良好"
            elif avg_score >= 70:
                rating = "⭐⭐⭐ 中等"
            elif avg_score >= 60:
                rating = "⭐⭐ 及格"
            else:
                rating = "⭐ 需努力"
            
            st.info(f"成绩评价：{rating}")

if __name__ == "__main__":
    main()
