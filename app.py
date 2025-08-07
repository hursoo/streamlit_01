import streamlit as st

st.set_page_config(page_title="Korean Text Analyzer", page_icon="🔎")

@st.cache_resource(show_spinner=False)
def load_analyzers():
    analyzer = None
    fallback = None
    reason = ""
    try:
        from kiwipiepy import Kiwi
        analyzer = Kiwi()
        # Warm-up
        analyzer.analyze("테스트 문장입니다.")
    except Exception as e:
        reason = str(e)
        try:
            from soynlp.tokenizer import LTokenizer
            # simple noun scoring from prebuilt scores (tiny demo)
            scores = {"한국": 1.0, "역사": 1.0, "분석": 1.0, "텍스트": 1.0}
            fallback = LTokenizer(scores)
        except Exception as e2:
            reason += " | soynlp fallback failed: " + str(e2)
    return analyzer, fallback, reason

analyzer, fallback, reason = load_analyzers()

st.title("한국어 텍스트 분석 데모 (Streamlit)")
st.write("kiwipiepy(kiwi)가 없으면 자동으로 soynlp 토크나이저로 폴백합니다.")

text = st.text_area("문장 입력", "개벽지에 실린 사설을 대상으로 형태소 분석을 시도합니다.", height=120)
do_pos = st.checkbox("품사 태깅(POS tagging) 보기", value=True)

if st.button("분석 실행"):
    if analyzer:
        result = analyzer.analyze(text)
        if do_pos:
            tokens = [f"{token.form}/{token.tag}" for sent in result for token in sent[0]]
        else:
            tokens = [token.form for sent in result for token in sent[0]]
        st.success("✅ kiwipiepy로 분석했습니다.")
        st.write(tokens)
    elif fallback:
        st.warning("⚠️ kiwipiepy 로드 실패. soynlp로 폴백합니다.")
        tokens = fallback.tokenize(text)
        st.write(tokens)
    else:
        st.error("분석기 로드 실패: " + reason)

with st.expander("환경 진단(Environment diagnostics)"):
    import sys, platform, subprocess
    st.write("Python:", sys.version)
    st.write("Platform:", platform.platform())
    try:
        import kiwipiepy
        st.write("kiwipiepy version:", kiwipiepy.__version__)
    except Exception:
        st.write("kiwipiepy not available.")
    try:
        import soynlp
        st.write("soynlp version:", soynlp.__version__)
    except Exception:
        st.write("soynlp not available.")
