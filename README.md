# CHATBOT - **PYTHON WEB**

## Mục Lục
[Khởi chạy project](#cài-môi-trường-ảo-và-setup-thư-viện)

[Khởi chạy project bằng `Docker` (nếu máy đã có docker)](#chạy-dự-án-bằng-dockerfile)

[Lưu ý dự án cần](#lưu-ý)

### Cài môi trường ảo và setup thư viện 
`Lưu ý`: 

* **Cài môi trường ảo**
```powershell
python -m venv .env
```

* **Active môi trường ảo**
```powershell
.env\Scripts\activate
```

* **Chạy lệnh cài toàn bộ thư viện cần thiết của dự án**
```powershell
pip install -r requirement.txt
```

* **Chạy dự án**
```
python main.py
```

Truy cập vào [localhost](http://localhost:80)

### Chạy dự án bằng Dockerfile
Hãy đảm bảo rằng `terminal` đang trỏ cùng thư mục với `dockerfile`
- **Build image**
```powershell
docker build -t ahihi:v1 .
```

- **Khởi chạy container**
```powershell
docker-compose up -d
```

Truy cập vào [localhost](http://localhost:80)

### Thư Mục Dư Án
```
📦app
 ┣ 📂bot
 ┃ ┣ 📜declaration_funcs.json
 ┃ ┣ 📜declaration_funcs.py
 ┃ ┣ 📜function_handler.py
 ┃ ┣ 📜generate_content.py
 ┃ ┣ 📜generate_history_chat.py
 ┃ ┣ 📜generate_image.py
 ┃ ┣ 📜generate_video.py
 ┃ ┗ 📜__init__.py
 ┣ 📂services
 ┃ ┣ 📜send_mail.py
 ┃ ┗ 📜__init__.py
 ┣ 📜models.py
 ┗ 📜__init__.py
```

### Lưu ý
Hãy đảm bảo rằng dự án bạn phải thỏa những điều kiện sau:
- Hãy trỏ `terminal/powershell` đúng thư mục của file main của dự án.
- Cài đặt toàn bộ thư viện mà dự án cần ở file [thư viện cần của dự án](./requirement.txt)
- Thiết lập các bộ phận cần thiết như (API keys, ...) tại file [setup.py](./setup.py)
