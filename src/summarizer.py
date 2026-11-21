import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

STYLE_INSTRUCTIONS = {
    "Ngắn gọn (3-5 ý chính)": (
        "Tóm tắt nội dung thành 3 đến 5 gạch đầu dòng súc tích nhất, "
        "tập trung vào thông điệp cốt lõi."
    ),
    "Chi tiết theo từng phần": (
        "Chia bản tóm tắt thành các đề mục rõ ràng (dùng Markdown ##), "
        "trình bày đầy đủ các luận điểm, ví dụ và số liệu quan trọng."
    ),
    "Trích xuất Action Items & Thuật ngữ": (
        "Liệt kê các hành động cụ thể có thể áp dụng ngay (Action Items) "
        "và giải thích ngắn gọn các thuật ngữ chuyên môn xuất hiện trong nội dung."
    ),
}


def summarize_content(text: str, style: str, language: str = "Tiếng Việt") -> str:
    """Gửi văn bản nguồn tới Gemini API và trả về bản tóm tắt định dạng Markdown."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa cấu hình GEMINI_API_KEY trong file .env")

    client = genai.Client(api_key=api_key)
    style_prompt = STYLE_INSTRUCTIONS.get(
        style, STYLE_INSTRUCTIONS["Chi tiết theo từng phần"]
    )

    system_instruction = (
        "Bạn là một trợ lý AI chuyên phân tích và tổng hợp thông tin chính xác, mạch lạc. "
        "Chỉ dựa trên nội dung được cung cấp, không tự suy diễn thông tin bên ngoài. "
        f"Trình bày toàn bộ kết quả bằng {language} dưới định dạng Markdown sạch đẹp."
    )

    user_prompt = f"""
Yêu cầu tóm tắt: {style_prompt}

--- NỘI DUNG NGUỒN ---
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
        ),
    )
    return response.text