# Hugging Face Spaces 또는 임의의 Docker 호스팅에 적합
FROM python:3.11-slim

# (선택) 시스템 패키지 설치
COPY packages.txt /tmp/packages.txt
RUN if [ -s /tmp/packages.txt ]; then           apt-get update &&           apt-get install -y --no-install-recommends $(tr '\n' ' ' < /tmp/packages.txt) &&           rm -rf /var/lib/apt/lists/*;         fi

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
# Streamlit 기본 포트 8501이지만, Spaces에서는 7860을 쓰기도 합니다.
ENV PORT=8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
