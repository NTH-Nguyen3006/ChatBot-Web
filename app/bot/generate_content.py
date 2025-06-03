import base64
import os
from google import genai
from google.genai import types
from .declaration_funcs import get_func_declaration_tool
from .function_handler import *
# from setup import GEMINI_KEYS
from setup import *


#retries = len(GEMINI_KEYS)-1
def generate_Content(prompt:str, attchment=None) -> str:
    client = genai.Client(
        # api_key=GEMINI_KEYS[retries],
        api_key="AIzaSyB6VIzIMt-Eax92Zt9GPQeiM0wE2KLo090"
    )
    model = "gemini-2.5-flash-preview-05-20" # Free: 10 RPM 500 req/day

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        tools=[get_func_declaration_tool()]
    )
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Nếu có ai hỏi bạn "ai đã sáng tạo ra bạn?" hoặc câu hỏi tương tự thì bạn hãy trả lời người sáng tạo ra bạn là 1 đội dev có các tên: 
                - Nguyễn Tấn Hoàng Nguyên
                - Phạm Thùy Trinh
                - Nguyễn Đài Vĩnh Khánh
                - Như Lê Hoàng Minh"""),
                types.Part.from_text(text="""Những dữ liệu đầu vào đó là những gì tôi huấn luyện bạn và bạn hãy học nó. Nếu dữ liệu đầu vào KHÔNG KHỚP hoặc không liên quan đến dữ liệu bạn đã được huấn luyện bao gồm cả HÀM mà tôi đã huấn luyện thì bạn hãy trả lời theo dữ liệu tự nhiên (gemini-2.5-flash) của bạn. Nếu đầu vào yêu cầu viết code thì bạn hãy viết code chi tiết (không gọi đến hàm, không hỏi lại yêu cầu) . Bạn hãy phản hồi người dùng theo cách tự nhiên nhất."""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    result_content = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):  
        print("Content: " ,chunk)
        if chunk.text: result_content += chunk.text
        elif chunk.function_calls:
            try:
                function_call = chunk.function_calls[0]
                # print(function_call)
                callback_func(function_call.name, function_call.args)
                result_content = generate_Content(
                    f"""Bạn hãy tạo ra 1 câu phản hồi đã hoàn thành công việc với công việc có nội dung: {function_call.model_dump_json()}.
                    Hãy tạo ra câu phản hồi mỗi lần khác nhau theo cách bạn sáng tạo tự nhiên nhất...""")
                # print("func call: ", result_content)
            except:
                generate_Content(prompt=prompt, attchment=attchment)
        
    print(result_content)

    return result_content




if __name__ == "__main__":
    # generate_Content("Xin chào")
    generate_Content("Hãy gửi mail đến \"nthn300607@gmail.com\" với Tiêu đề là \"ABC\". Nội dung bạn hãy viết như sau: Hello xin chào bạn")
