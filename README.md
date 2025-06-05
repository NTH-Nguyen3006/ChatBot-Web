# CHATBOT - PYTHON WEB

## Mục Lục
[Khởi chạy project](#cài-môi-trường-ảo-và-setup-thư-viện)

[Khởi chạy project bằng Docker (nếu máy đã có docker)](#cài-môi-trường-ảo-và-setup-thư-viện)

### Cài môi trường ảo và setup thư viện 
- `Lưu ý`: hãy trỏ `terminal/powershell` đúng thư mục của file main của dự án.

* Cài môi trường ảo
```powershell
python -m venv .env
```

* Active môi trường ảo
```powershell
.env\Scripts\activate
```

* Chạy lệnh cài toàn bộ thư viện cần thiết của dự án
```powershell
pip install -r requirement.txt
```

* Chạy dự án 
```
python main.py
```

Truy cập vào [localhost](localhost:80)

### Chạy dự án bằng Dockerfile
- Build image
```powershell
docker build -t ahihi:v1 .
```

- Khởi chạy container 
```powershell
docker-compose up -d
```

Truy cập vào [localhost](localhost:80)
