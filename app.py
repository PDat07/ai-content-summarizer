import streamlit as st
from src.extractors import (
    extract_pdf_text,
    extract_txt_text,
    get_youtube_transcript,
)
from src.summarizer import STYLE_INSTRUCTIONS, summarize_content

st.set_page_config(
    page_title="AI Video & Document Summarizer",
    page_icon="📑",
    layout="centered",
)

st.title("📑 AI Video & Document Summarizer")
st.caption("Tóm tắt nhanh video YouTube hoặc tài liệu PDF/TXT bằng Gemini AI")

# Thanh tùy chỉnh bên trái
with st.sidebar:
    st.header("⚙️ Tùy chỉnh")
    style = st.selectbox("Phong cách tóm tắt", list(STYLE_INSTRUCTIONS.keys()))
    language = st.selectbox("Ngôn ngữ đầu ra", ["Tiếng Việt", "English"])
    st.markdown("---")
    st.markdown("💡 **Mẹo:** Với PDF, hãy dùng file có lớp văn bản (không phải ảnh scan).")

# Chia 2 tab nguồn dữ liệu
tab_yt, tab_doc = st.tabs(["🎥 Link YouTube", "📄 Tải lên tài liệu"])

with tab_yt:
    youtube_url = st.text_input(
        "Dán đường dẫn video YouTube:",
        placeholder="https://www.youtube.com/watch?v=...",
    )
    if st.button("Tóm tắt Video", type="primary", use_container_width=True):
        if not youtube_url.strip():
            st.warning("Vui lòng nhập link YouTube.")
        else:
            try:
                with st.spinner("Đang lấy phụ đề video..."):
                    raw_text = get_youtube_transcript(youtube_url)
                with st.spinner("AI đang phân tích và tóm tắt..."):
                    st.session_state["summary"] = summarize_content(
                        raw_text, style, language
                    )
            except Exception as e:
                st.error(str(e))

with tab_doc:
    uploaded_file = st.file_uploader(
        "Chọn file tài liệu (.pdf hoặc .txt):", type=["pdf", "txt"]
    )
    if st.button("Tóm tắt Tài liệu", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.warning("Vui lòng tải lên một file.")
        else:
            try:
                with st.spinner("Đang trích xuất nội dung file..."):
                    if uploaded_file.name.endswith(".pdf"):
                        raw_text = extract_pdf_text(uploaded_file)
                    else:
                        raw_text = extract_txt_text(uploaded_file)
                with st.spinner("AI đang phân tích và tóm tắt..."):
                    st.session_state["summary"] = summarize_content(
                        raw_text, style, language
                    )
            except Exception as e:
                st.error(str(e))

# Hiển thị kết quả và nút tải xuống
if "summary" in st.session_state and st.session_state["summary"]:
    st.markdown("---")
    st.subheader("✨ Kết quả tóm tắt")
    st.markdown(st.session_state["summary"])

    st.download_button(
        label="⬇️ Tải xuống bản tóm tắt (.md)",
        data=st.session_state["summary"],
        file_name="summary.md",
        mime="text/markdown",
    )