# Streamlit + kiwipiepy Starter

한국어 형태소 분석기 **kiwipiepy** 중심의 Streamlit 데모입니다.
- Streamlit Cloud 배포 시 `runtime.txt`로 Python을 3.11로 고정
- `requirements.txt`는 최소 의존성만 명시 (서버가 호환 버전 자동 선택)

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud
1. 이 폴더를 깃허브에 올립니다.
2. Streamlit Cloud에서 새 앱을 만들고 이 리포를 연결합니다.
3. `runtime.txt`(python-3.11)와 간소화된 `requirements.txt`를 유지하세요.

## Hugging Face Spaces (Docker로 강제 제어)
`Dockerfile`과 `packages.txt`를 함께 사용하세요. (리포에 포함)
