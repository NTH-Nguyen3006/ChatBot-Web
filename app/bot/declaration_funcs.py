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

# Generation Config with Function Declaration
_tools = types.Tool(function_declarations=func_declarations)
config = types.GenerateContentConfig(tools=[_tools])

# Define user prompt
contents = [
    types.Content(
        role="user", parts=[types.Part(text="Tạo giúp cho tôi một bức ảnh con mèo")]
    )
]

# Send request with function declarations
# response = client.models.generate_content(
#     model="gemini-2.0-flash", config=config, contents=contents
# )

# print(response.candidates[0].content.parts[0].function_call)