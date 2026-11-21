import re
import fitz  # Thư viện PyMuPDF
from youtube_transcript_api import YouTubeTranscriptApi


def extract_youtube_id(url: str) -> str | None:
    """Tách video ID (11 ký tự) từ các định dạng link YouTube phổ biến."""
    pattern = r"(?:v=|\/|be\/|shorts\/)([0-9A-Za-z_-]{11})(?:[?&\/]|$)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_youtube_transcript(url: str) -> str:
    """Lấy toàn bộ phụ đề của video YouTube (ưu tiên tiếng Việt, sau đó tiếng Anh)."""
    video_id = extract_youtube_id(url)
    if not video_id:
        raise ValueError("Link YouTube không hợp lệ. Vui lòng kiểm tra lại.")

    try:
        if hasattr(YouTubeTranscriptApi, "get_transcript"):
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=["vi", "en"]
            )
            return " ".join(item["text"] for item in transcript)
        else:
            api = YouTubeTranscriptApi()
            transcript = api.fetch(video_id, languages=["vi", "en"])
            return " ".join(snippet.text for snippet in transcript)
    except Exception as e:
        raise RuntimeError(
            f"Không thể lấy phụ đề (video có thể đã tắt phụ đề hoặc không hỗ trợ): {e}"
        )


def extract_pdf_text(uploaded_file) -> str:
    """Trích xuất văn bản từ file PDF tải lên Streamlit."""
    try:
        file_bytes = uploaded_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages_text = [page.get_text("text") for page in doc]
        full_text = "\n".join(pages_text).strip()

        if not full_text:
            raise ValueError(
                "Không tìm thấy văn bản trong PDF (có thể đây là file scan dạng ảnh)."
            )
        return full_text
    except Exception as e:
        raise RuntimeError(f"Lỗi khi đọc file PDF: {e}")


def extract_txt_text(uploaded_file) -> str:
    """Đọc nội dung file văn bản thuần (.txt)."""
    return uploaded_file.read().decode("utf-8", errors="ignore").strip()