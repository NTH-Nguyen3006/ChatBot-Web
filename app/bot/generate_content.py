import base64
import os
from google import genai
from google.genai import types
from declaration_funcs import _tools
from function_handler import *
# from setup import GEMINI_KEYS

#retries = len(GEMINI_KEYS)-1
def generate_Content(promt:str):
    client = genai.Client(
        # api_key=GEMINI_KEYS[retries],
        api_key="AIzaSyB6VIzIMt-Eax92Zt9GPQeiM0wE2KLo090"
    )
    model = "gemini-2.5-flash-preview-05-20"

    generate_content_config = types.GenerateContentConfig(
        # response_mime_type="text/plain",
        tools=[_tools]
    )
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=promt),
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
            callback_func(function_call.name, function_call.args)
            

        print(chunk.model_dump_json())




    return result_content

if __name__ == "__main__":
    # generate_Content("Xin chào")
    generate_Content("Hãy tạo cho tôi 1 bức ảnh mèo, yêu cầu hình ảnh phải chân thật")
