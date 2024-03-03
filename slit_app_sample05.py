import streamlit as st
import pandas as pd
import altair as alt
import chardet

# Streamlitアプリのタイトル
st.title('作業グループごとの時系列作業数分析')

# データアップロードのセクション
uploaded_file = st.file_uploader("ファイルをアップロードしてください（CSV形式）", type="csv")
if uploaded_file is not None:
    # ファイルのエンコーディングを検出
    raw_data = uploaded_file.read()
    encoding = chardet.detect(raw_data)['encoding']
    uploaded_file.seek(0)  # ファイルポインタをリセット
    
    # エンコーディングを指定してデータフレームに読み込む
    df = pd.read_csv(uploaded_file, encoding=encoding)

    # '開始時刻'から'hour'を抽出
    df['hour'] = pd.to_datetime(df['開始時刻'], format='%H:%M:%S').dt.hour

    # ユニークな「作業グループ」を取得し、色の辞書を作成
    work_groups = df['作業グループ'].unique()
    # カラースキームを定義
    colors = alt.Scale(range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])

    # Altairチャートを作成するための空のデータフレームを準備
    chart = alt.Chart(df).mark_line()

    # '作業グループ'で色分けをして、'hour'ごとの'作業数'の平均を描画
    chart = alt.Chart(df).mark_line().encode(
        x='hour:O',
        y=alt.Y('average(作業数):Q', title='平均作業数'),
        color=alt.Color('作業グループ:N', scale=colors),
        tooltip=['hour:N', 'average(作業数):Q', '作業グループ:N']
    ).properties(
        width=700,
        height=400
    )

    # チャートを表示
    st.altair_chart(chart, use_container_width=True)
else:
    st.info('データファイルをアップロードして分析を開始してください。')
