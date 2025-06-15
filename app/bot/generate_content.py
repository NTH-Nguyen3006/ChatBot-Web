import base64, os, logging
from google import genai
from google.genai import types
from .declaration_funcs import get_func_declaration_tool
from .function_handler import *
# from setup import GEMINI_KEYS
from setup import *


#retries = len(GEMINI_KEYS)-1
def generate_Content(prompt:str, attchment=None, retries = len(GEMINI_KEYS)-1) -> dict:
    client = genai.Client(
        api_key=GEMINI_KEYS[retries],
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
                - Như Lê Hoàng Minh
                Bạn hãy ngừng đề cập đến Google đã huấn luyện ra bạn"""),
                types.Part.from_text(text="""Bạn là một trợ lý AI toàn diện. Mặc dù bạn có khả năng đặc biệt trong việc gọi hàm để thực hiện các tác vụ và truy xuất thông tin cụ thể, nhưng điều đó không giới hạn kiến thức và khả năng của bạn.
**Vai trò của bạn:**
* **Hỗ trợ mọi lĩnh vực:** Bạn có thể trả lời các câu hỏi, cung cấp thông tin và hỗ trợ thảo luận về bất kỳ chủ đề nào, từ khoa học, lịch sử, văn hóa, công nghệ đến các vấn đề thường ngày, và nhiều hơn nữa.
* **Sử dụng kiến thức tổng quát:** Hãy truy cập vào toàn bộ kiến thức rộng lớn mà bạn đã được đào tạo để cung cấp câu trả lời đầy đủ và chính xác nhất.
* **Tận dụng khả năng gọi hàm:** Khi một câu hỏi hoặc yêu cầu cần thông tin chi tiết, dữ liệu thời gian thực, hoặc một hành động cụ thể, hãy sử dụng các hàm đã được tích hợp (ví dụ: tìm kiếm thông tin, truy xuất dữ liệu, thực hiện tính toán) để bổ sung và làm phong phú câu trả lời của bạn. Việc gọi hàm là một công cụ giúp bạn cung cấp câu trả lời tốt hơn, không phải là một giới hạn.
* **Ưu tiên dữ liệu huấn luyện cụ thể:** Trong trường hợp có các câu hỏi liên quan đến dữ liệu hoặc chức năng mà tôi đã đặc biệt huấn luyện bạn (ví dụ: các hàm API cụ thể, thông tin huấn luyện, ...), hãy ưu tiên sử dụng và trình bày thông tin đó một cách chính xác. Tuy nhiên, nếu câu hỏi vượt ra ngoài phạm vi dữ liệu huấn luyện cụ thể này, bạn vẫn có thể sử dụng kiến thức tổng quát của mình. Trường hợp câu hỏi yêu cầu bạn viết code thì bạn không nên thực thi nó, mà chỉ viết thôi.
* **Trả lời chân thật và thực tế:** Luôn cung cấp thông tin dựa trên dữ kiện, dữ liệu đáng tin cậy. Tránh đưa ra ý kiến cá nhân, suy đoán hoặc thông tin chưa được xác minh. Nếu bạn không biết hoặc không chắc chắn về một thông tin, hãy nói rõ điều đó. Mục tiêu của bạn là cung cấp câu trả lời hữu ích, chính xác và đáng tin cậy nhất cho người dùng.
**Khi bạn tương tác:**
* Lắng nghe kỹ câu hỏi của người dùng.
* Xác định liệu có cần sử dụng hàm để trả lời tốt hơn hay không.
* Nếu cần, hãy sử dụng hàm một cách thông minh và sau đó tích hợp kết quả vào câu trả lời tự nhiên.
* Đảm bảo câu trả lời rõ ràng, dễ hiểu và phù hợp với ngữ cảnh.
Bắt đầu từ bây giờ, hãy là một trợ lý AI toàn diện và thông thái!\n\n\n"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    model_response = {"message": "", 'image': None}
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):  
        print("Content: " ,chunk.text)
        if chunk.text: model_response["message"] += chunk.text
        elif chunk.function_calls:
            try:
                function_call = chunk.function_calls[0]
                # print(function_call)
                response = callback_func(function_call.name, function_call.args)
                print(response)
                if response["content"]:
                    model_response["message"] = response.get("content", "Tôi là AHIHI. Chatbot vạn năng")
                if response["image"]:
                    model_response["image"] = response.get("image", None)

                # result_content = generate_Content(
                #     f"""Bạn hãy tạo ra 1 câu phản hồi đã hoàn thành công việc với công việc có nội dung: {function_call.model_dump_json()}.
                #     Hãy tạo ra câu phản hồi mỗi lần khác nhau theo cách bạn sáng tạo tự nhiên và thông thái nhất...""")
                
            except Exception as e:
                print(e)
                if (retries == -1): return "Đã xảy ra lỗi. Tôi là AHIHI. Chatbot vạn năng"
                return generate_Content(prompt=prompt, attchment=attchment, retries=retries-1)
        
    return model_response


if __name__ == "__main__":
    # generate_Content("Xin chào")
    generate_Content("Hãy gửi mail đến \"nthn300607@gmail.com\" với Tiêu đề là \"ABC\". Nội dung bạn hãy viết như sau: Hello xin chào bạn")
