FROM python:3.8-buster

# 作業ディレクトリの設定
WORKDIR /app

# OSパッケージのアップデートと必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y gcc libffi-dev musl-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 必要なPythonパッケージのインストール
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# アプリケーションのコードをコピー
COPY . /app

# Streamlitのポートを開放
EXPOSE 8501

# アプリケーションの実行
CMD ["streamlit", "run", "slit_app_sample01.py"]
