import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import platform

st.set_page_config(page_title="나만의 텍스트 분석기", page_icon="🥝")

st.title("🥝 나만의 텍스트 분석 도우미 (Kiwi 우선, soynlp 폴백)")
st.write("txt 파일을 업로드하면 명사 추출, 빈도 분석, 워드클라우드를 보여줍니다.")

# --- 분석기 로드 함수 ---
@st.cache_resource(show_spinner=False)
def load_analyzer():
    analyzer = None
    fallback = None
    reason = ""
    try:
        from kiwipiepy import Kiwi
        analyzer = Kiwi()
        analyzer.analyze("테스트 문장입니다.")
    except Exception as e:
        reason = str(e)
        try:
            from soynlp.tokenizer import LTokenizer
            scores = {"한국": 1.0, "역사": 1.0, "분석": 1.0, "텍스트": 1.0}
            fallback = LTokenizer(scores)
        except Exception as e2:
            reason += " | soynlp fallback failed: " + str(e2)
    return analyzer, fallback, reason

analyzer, fallback, reason = load_analyzer()

# --- 파일 업로드 ---
uploaded_file = st.file_uploader("분석할 텍스트 파일(txt)을 선택하세요.", type="txt")

if uploaded_file is not None:
    # 파일 읽기 (UTF-8 우선, 실패 시 CP949)
    try:
        raw_text = uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        raw_text = uploaded_file.read().decode('cp949')

    st.subheader("📝 원본 텍스트")
    st.text_area("내용", raw_text, height=200)

    # --- 형태소 분석 ---
    if analyzer:
        result = analyzer.analyze(raw_text)
        nouns = [token.form for sent in result for token in sent[0] if token.tag in ['NNG', 'NNP']]
    elif fallback:
        nouns = [tok for tok in fallback.tokenize(raw_text) if len(tok) > 1]
        st.warning("⚠️ kiwipiepy 로드 실패. soynlp로 분석합니다.")
    else:
        st.error("분석기 로드 실패: " + reason)
        nouns = []

    # 1글자 단어 제거
    words = [n for n in nouns if len(n) > 1]

    # --- 빈도 분석 ---
    count = Counter(words)
    most_common_words = count.most_common(30)

    st.subheader("📊 단어 빈도 분석 (상위 30개)")
    df = pd.DataFrame(most_common_words, columns=['단어', '빈도수'])
    st.dataframe(df)

    # --- 워드클라우드 ---
    st.subheader("☁️ 워드클라우드")
    # 폰트 경로 자동 선택
    if platform.system() == "Windows":
        font_path = "c:/Windows/Fonts/malgun.ttf"
    elif platform.system() == "Darwin":  # macOS
        font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
    else:  # Linux (Streamlit Cloud)
        font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
        if not os.path.exists(font_path):
            st.warning("기본 한글 폰트를 찾지 못했습니다. 워드클라우드 한글이 깨질 수 있습니다.")

    try:
        wc = WordCloud(font_path=font_path, background_color='white', width=800, height=600)
        cloud = wc.generate_from_frequencies(dict(most_common_words))
        fig, ax = plt.subplots()
        ax.imshow(cloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"워드클라우드 생성 실패: {e}")

# --- 환경 진단 ---
with st.expander("환경 진단(Environment diagnostics)"):
    import sys
    st.write("Python:", sys.version)
    try:
        import kiwipiepy
        st.write("kiwipiepy version:", kiwipiepy.__version__)
    except ImportError:
        st.write("kiwipiepy not available.")
    try:
        import soynlp
        st.write("soynlp version:", soynlp.__version__)
    except ImportError:
        st.write("soynlp not available.")
