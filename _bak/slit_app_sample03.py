# 必要なライブラリのインポート
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chardet
from datetime import datetime

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

    # 数値型の列（'作業数', '作業数2', '作業数3'）が数値型であることを確認し、変換が必要な場合は変換
    for column in ['作業数', '作業数2', '作業数3']:
        if not np.issubdtype(df[column].dtype, np.number):
            df[column] = pd.to_numeric(df[column], errors='coerce')

    # '開始時刻'と'終了時刻'から'datetime'列を生成
    df['開始datetime'] = pd.to_datetime(df['日付'] + ' ' + df['開始時刻'])
    df['hour'] = df['開始datetime'].dt.hour

    # データの前処理
    df.fillna(method='ffill', inplace=True)

    # 基本統計の表示
    if st.checkbox('基本統計を表示'):
        st.write(df.describe())

    # 時間帯ごとの各作業数の平均を表示
    for work_number in ['作業数', '作業数2', '作業数3']:
        efficiency_by_hour = df.groupby('hour')[work_number].mean()
        st.subheader(f'時間帯ごとの{work_number}の平均')
        st.line_chart(efficiency_by_hour)
else:
    st.info('データファイルをアップロードして分析を開始してください。')
