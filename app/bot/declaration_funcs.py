from google import genai
from google.genai import types

generate_image_declaration = {
    'name': "generateImage",
    "description": "Hàm tạo hình ảnh từ Gemini",
    'parameters': {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": """Tin nhắn từ người dùng yêu cầu tạo hình ảnh, 
                hãy lấy đoạn text yêu cầu tạo ảnh từ người dùng và soạn cú pháp "tạo hình ảnh <yêu cầu>" rồi truyền vào hàm.
                """,
            }
        },
    },
    # "required": ["prompt"]
}   

func_declarations = [generate_image_declaration]
_tools = types.Tool(function_declarations=func_declarations)
