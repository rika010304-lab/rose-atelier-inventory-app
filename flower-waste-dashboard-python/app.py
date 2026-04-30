import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Rose Waste Dashboard",
    page_icon="🌹",
    layout="wide"
)

st.title("🌹 廃棄データ可視化ダッシュボード")
st.write("バラの廃棄データを集計し、ロスの傾向を確認できます。")

@st.cache_data
def load_data():
    return pd.read_csv("waste_records.csv")

df = load_data()
uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSVを読み込みました")
df["date"] = pd.to_datetime(df["date"])

st.sidebar.header("絞り込み")

colors = ["すべて"] + sorted(df["color"].unique().tolist())
selected_color = st.sidebar.selectbox("色", colors)

reasons = ["すべて"] + sorted(df["reason"].unique().tolist())
selected_reason = st.sidebar.selectbox("廃棄理由", reasons)

filtered_df = df.copy()

if selected_color != "すべて":
    filtered_df = filtered_df[filtered_df["color"] == selected_color]

if selected_reason != "すべて":
    filtered_df = filtered_df[filtered_df["reason"] == selected_reason]

total_waste = filtered_df["quantity"].sum()
total_records = len(filtered_df)
top_variety = (
    filtered_df.groupby("variety")["quantity"].sum().idxmax()
    if not filtered_df.empty else "-"
)

col1, col2, col3 = st.columns(3)

col1.metric("廃棄合計本数", f"{total_waste}本")
col2.metric("廃棄記録数", f"{total_records}件")
col3.metric("最も廃棄が多い品種", top_variety)

st.divider()

st.subheader("月別 廃棄本数")

df["month"] = df["date"].dt.to_period("M").astype(str)
monthly = df.groupby("month")["quantity"].sum()

fig3, ax3 = plt.subplots()
ax3.plot(monthly.index, monthly.values, marker="o")
ax3.set_xlabel("月")
ax3.set_ylabel("廃棄本数")
plt.xticks(rotation=45)

st.pyplot(fig3)
st.subheader("品種別 廃棄本数")
variety_summary = filtered_df.groupby("variety")["quantity"].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
ax1.bar(variety_summary.index, variety_summary.values)
ax1.set_xlabel("品種")
ax1.set_ylabel("廃棄本数")
ax1.tick_params(axis="x", rotation=45)
st.pyplot(fig1)

st.subheader("色別 廃棄本数")
color_summary = filtered_df.groupby("color")["quantity"].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
ax2.bar(color_summary.index, color_summary.values)
ax2.set_xlabel("色")
ax2.set_ylabel("廃棄本数")
st.pyplot(fig2)

st.subheader("廃棄理由別 集計")
reason_summary = filtered_df.groupby("reason")["quantity"].sum().sort_values(ascending=False)
st.dataframe(reason_summary.reset_index().rename(columns={"quantity": "廃棄本数"}))

st.subheader("廃棄データ一覧")
st.dataframe(filtered_df)