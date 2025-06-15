import requests

def light_control(status="off"):
    from ..bot import generate_Content
    IP = "192.168.1.6"
    requests.get(f"http://{IP}/{status.lower()}")

    return {
        "content": generate_Content(f"Bạn hãy phản hồi người dùng về hành động bạn đã làm xong nhiệm vụ {status} đèn. Hành động này không cần phải call function")["message"],
        "image": []
    }