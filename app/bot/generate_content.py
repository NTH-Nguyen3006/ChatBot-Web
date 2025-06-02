import base64
import os
from google import genai
from google.genai import types
from .declaration_funcs import get_func_declaration_tool
from .function_handler import *
# from setup import GEMINI_KEYS

#retries = len(GEMINI_KEYS)-1
def generate_Content(prompt:str) -> str:
    client = genai.Client(
        # api_key=GEMINI_KEYS[retries],
        api_key="AIzaSyB6VIzIMt-Eax92Zt9GPQeiM0wE2KLo090"
    )
    model = "gemini-2.5-flash-preview-05-20" # Free: 10 RPM 500 req/day

    generate_content_config = types.GenerateContentConfig(
        # response_mime_type="text/plain",
        tools=[get_func_declaration_tool()]
    )
    contents = [
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
        if chunk.text: result_content += chunk.text
        elif chunk.function_calls:
            function_call = chunk.function_calls[0]
            print(function_call)
            callback_func(function_call.name, function_call.args)
            result_content = generate_Content(
                f"Bạn hãy tạo ra 1 câu trả lời đã hoàn thành nhiệm vụ với nhiệm vụ là: {function_call.model_dump_json()}")
            
        print("Content: " ,chunk.text)

    return result_content

generate_Content("Hãy gửi mail đến nthn300607@gmail.com  với Tiêu đề là \"ABC\". Nội dung bạn hãy viết như sau: Hello xin chào bạn")


if __name__ == "__main__":
    # generate_Content("Xin chào")
    generate_Content("Hãy gửi mail đến \"nthn300607@gmail.com\" với Tiêu đề là \"ABC\". Nội dung bạn hãy viết như sau: Hello xin chào bạn")
