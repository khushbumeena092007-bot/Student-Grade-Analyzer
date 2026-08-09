import streamlit as st
import matplotlib.pyplot as plt
from gradeAnalyser import GradeAnalyser

st.set_page_config(page_title="Student Grade Analyzer", page_icon="🎓", layout="wide")

st.title("🎓 Student Grade Analyzer")
st.write("upload a csv file to generate report")
uploaded_file= st.file_uploader(
    "upload student csv",
    type=["csv"]
)

if uploaded_file:
    with st.spinner("Generating Reports......"):


        (
            df,
            class_summary,
            Gender_summary,
            Class_Gender_summary,
            City_Class_Summary,
            top_10,
            bottam_10,
            At_Risk,
            failure_rate,
            Demography
        ) = GradeAnalyser(uploaded_file)

    # ---------------- Dashboard ----------------
    st.header("📊 Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Students", len(df))
    c2.metric("Classes", df["Class"].nunique())
    c3.metric("Cities", df["City"].nunique())
    c4.metric("Average %", round(df["percentage"].mean(), 2))

    st.divider()

    # ---------------- Graphs ----------------
    
    st.header("📊 Graphs")

    col1, col2 = st.columns(2)

    with col1:
        st.image("graphs/class_bar.png", caption="Class Average")

    with col2:
        st.image("graphs/subject_Average.png", caption="Subject Average")

    col3, col4 = st.columns(2)

    with col3:
        st.image("graphs/result_bar.png", caption="Pass vs Fail")

    with col4:
        st.image("graphs/Attendance_chart.png", caption="Attendance Distribution")

    col5, col6=st.columns(2)
    with col5:
        st.image("graphs/gender_distribution.png", caption="Gender Distribution")

    with col6:
        st.image("graphs/Class_strength.png",caption="Class Strength")

    st.image("graphs/AttendanceVS_percentage.png")

    st.divider()

    # ---------------- Students ----------------
    st.header("📋 Student Records")
    st.dataframe(df)

    st.divider()

    # ---------------- Top & Bottom ----------------
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("🏆 Top 10 Students")
        st.dataframe(top_10)

    with col6:
        st.subheader("📉 Bottom 10 Students")
        st.dataframe(bottam_10)

    st.divider()

    # ---------------- At Risk ----------------
    st.header("⚠️ At Risk Students")
    st.dataframe(At_Risk)
    st.divider()

    # ---------------- Summaries ----------------
    st.header("📚 Class Summary")
    st.dataframe(class_summary)

    st.header("👨‍🎓 Gender Summary")
    st.dataframe(Gender_summary)

    st.header("👥 Class Gender Summary")
    st.dataframe(Class_Gender_summary)

    st.header("🏙️ City Class Summary")
    st.dataframe(City_Class_Summary)

    st.divider()

    # ---------------- Failure Rate ----------------
    st.header(" 🚩Subject-wise Failure Rate")
    st.dataframe(failure_rate)

    st.divider()

    # ---------------- Demography ----------------
    st.header("🌍 Demography")

    for key, value in Demography.items():
        st.subheader(key.replace("_", " ").title())
        st.dataframe(value.reset_index())

    st.divider()

    # ---------------- Download ----------------
    with open("student_Grade_Reports.xlsx", "rb") as f:
        st.download_button(
            "📥 Download Student Grade Report",
            data=f,
            file_name="student_Grade_Reports.xlsx"
        )

    with open("Students_Classwise_Reports.xlsx", "rb") as f:
        st.download_button(
            "📥 Download Classwise Report",
            data=f,
            file_name="Students_Classwise_Reports.xlsx"
        )