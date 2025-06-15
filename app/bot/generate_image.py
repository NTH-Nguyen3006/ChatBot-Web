from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from setup import GEMINI_KEYS
import base64

def generateImage(prompt, retries=0):
    from . import generate_Content
    print(prompt)
    try:
        client = genai.Client( api_key="AIzaSyB6VIzIMt-Eax92Zt9GPQeiM0wE2KLo090")
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
            )
        )
        result = {"content": "", 'image': []}
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                result["image"] = "data:image/png;base64," + base64.b64encode(part.inline_data.data).decode() 
                result['content'] += generate_Content("Cho tôi 1 câu phản hồi đã hoàn thành việc tạo ảnh. Kiểu tự nhiên và thông thái")["message"]
                image.save('gemini-native-image.png')
                image.show()
        return result
    except Exception as e:
        print("Lỗi tạo ảnh Gemini: ", e)
        if retries == len(GEMINI_KEYS) - 1:
            return {"content": "Có thể đã lỗi bên kĩ thuật", 'image': ""}
        return generateImage(prompt=prompt, retries=retries+1)

if __name__ == "__main__" :
    generateImage('tạo ảnh cận cảnh một người phụ nữ ở độ tuổi 20, ảnh đường phố, ảnh tĩnh trong phim, tông màu cam ấm dịu')