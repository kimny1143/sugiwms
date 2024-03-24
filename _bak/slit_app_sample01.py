import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chardet

# Streamlitアプリのタイトル
st.title('物流業務効率分析ダッシュボード')

# データアップロードのセクション
uploaded_file = st.file_uploader("ファイルをアップロードしてください（CSV形式）", type="csv")
if uploaded_file is not None:
    # ファイルのエンコーディングを検出
    raw_data = uploaded_file.read()
    encoding = chardet.detect(raw_data)['encoding']
    uploaded_file.seek(0)  # ファイルポインタをリセット
    
    # エンコーディングを指定してデータフレームに読み込む
    df = pd.read_csv(uploaded_file, encoding=encoding)

    # データの前処理
    df.fillna(method='ffill', inplace=True)

    # 基本統計の表示
    if st.checkbox('基本統計を表示'):
        st.write(df.describe())

    # 業務効率分析
    if 'timestamp' in df.columns:
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        efficiency_by_hour = df.groupby('hour').mean()['efficiency_metric']

        st.subheader('時間帯ごとの業務効率')
        fig, ax = plt.subplots()
        sns.lineplot(data=efficiency_by_hour, ax=ax)
        ax.set(title='Hourly Efficiency', xlabel='Hour of the Day', ylabel='Efficiency Metric')
        st.pyplot(fig)

        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        efficiency_by_date = df.groupby('date').mean()['efficiency_metric']

        st.subheader('日別の業務効率')
        fig, ax = plt.subplots()
        sns.lineplot(data=efficiency_by_date, ax=ax)
        ax.set(title='Daily Efficiency', xlabel='Date', ylabel='Efficiency Metric')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.error('timestamp列が見つかりません。データを確認してください。')
else:
    st.info('データファイルをアップロードして分析を開始してください。')
