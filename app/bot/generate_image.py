from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

def generateImage(prompt):
    client = genai.Client(
        api_key="AIzaSyB6VIzIMt-Eax92Zt9GPQeiM0wE2KLo090"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )

    print(response.candidates[0].content.parts)
    result = {"contents": [], 'images': []}
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
            result["contents"].append(part.text)  
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            print(base64.b64encode(part.inline_data.data))
            result["images"].append(base64.b64encode(part.inline_data.data))  
            image.save('gemini-native-image.png')
            image.show()

    return result


if __name__ == "__main__" :
    generateImage('tạo ảnh cận cảnh một người phụ nữ ở độ tuổi 20, ảnh đường phố, ảnh tĩnh trong phim, tông màu cam ấm dịu')