import base64
import os
from google import genai
from google.genai import types
# from setup import GEMINI_KEYS

#retries = len(GEMINI_KEYS)-1
def generate_Content(promt:str):
    client = genai.Client(
        # api_key=GEMINI_KEYS[retries],
        api_key="AIzaSyB6VIzIMt-Eax92Zt9GPQeiM0wE2KLo090"
    )
    model = "gemini-2.5-flash-preview-05-20"
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text='Nếu người dùng (user) có yêu cầu bạn tạo 1 bức ảnh thì bạn hãy trả về 1 từ khóa "Generate_Image_Ahihi" cho tôi để tôi xử lý'),
            ],
        ),

        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=promt),
            ],
        ),
    ]



    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.model_dump_json(), end="")

    return chunk.text

if __name__ == "__main__":
    generate_Content("Hãy tạo cho tôi 1 bức ảnh con mèo ")
