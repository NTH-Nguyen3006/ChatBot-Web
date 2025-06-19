from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from setup import GEMINI_KEYS
import base64, mimetypes

def generateImage(prompt, attchment=None, retries=0):
    # from . import generate_Content
    try:
        client = genai.Client(api_key=GEMINI_KEYS[retries])
        parts = [ types.Part.from_text(text=prompt), ]
        if attchment is not None:
            parts.append(types.Part.from_bytes(
                mime_type="image/jpeg", data=base64.b64decode(attchment)
            ))
            
        contents = [ types.Content(role="user", parts=parts) ]
        generate_content_config = types.GenerateContentConfig(
            response_modalities=[ "IMAGE", "TEXT"],
            response_mime_type="text/plain",
        )
        content_stream = client.models.generate_content_stream(
            model="gemini-2.0-flash-preview-image-generation",
            contents=contents,
            config=generate_content_config,
        )

        result = {"content": "", 'image': []}
        for chunk in content_stream:
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ): continue
            if (chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data):
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                data_buffer = inline_data.data
                result["image"] = "data:image/png;base64," + base64.b64encode(data_buffer).decode() 
            else:
                result['content'] += chunk.text
        
        # response = client.models.generate_content(
        #     model="gemini-2.0-flash-preview-image-generation",
        #     contents=prompt,
        #     config=types.GenerateContentConfig(
        #     response_modalities=['TEXT', 'IMAGE']
        #     )
        # )
        # for part in response.candidates[0].content.parts:
        #     if part.inline_data is not None:
        #         image = Image.open(BytesIO((part.inline_data.data)))
        #         result["image"] = "data:image/png;base64," + base64.b64encode(part.inline_data.data).decode() 
        #         result['content'] += generate_Content("Cho tôi 1 câu phản hồi đã hoàn thành việc tạo ảnh. Kiểu tự nhiên và thông thái")["message"]
                # image.save('gemini-native-image.png')
                # image.show()
        return result
    except Exception as e:
        print("Lỗi tạo ảnh Gemini: ", e)
        if retries == len(GEMINI_KEYS) - 1:
            return {"content": "Có thể đã lỗi bên kĩ thuật", 'image': ""}
        return generateImage(prompt=prompt, retries=retries+1)

if __name__ == "__main__" :
    generateImage('tạo ảnh cận cảnh một người phụ nữ ở độ tuổi 20, ảnh đường phố, ảnh tĩnh trong phim, tông màu cam ấm dịu')