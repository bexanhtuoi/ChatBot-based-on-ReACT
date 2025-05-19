# Hướng dẫn chạy dự án AI ChatBot (React + FastAPI)

## 1. Yêu cầu môi trường
- Python 3.9 trở lên
- Node.js 18+ và npm
- (Khuyến nghị) Sử dụng Windows Terminal hoặc PowerShell

## 2. Cấu trúc dự án
```
ReACT_Agent/
├── back-end/      # FastAPI server
├── font-end/      # React client
```

## 3. Chạy back-end (FastAPI)
### a. Cài đặt thư viện Python
```powershell
cd back-end
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### b. Tạo file .env (nếu chưa có)
```
GEMINI_API_KEY="<your_gemini_api_key>"
TAVILY_API_KEY="<your_tavily_api_key>"
```

### c. Chạy server FastAPI
```powershell
uvicorn main:app --reload
```
- Server mặc định chạy ở http://localhost:8000

## 4. Chạy font-end (React)
### a. Cài đặt package
```powershell
cd font-end
npm install
```
### b. Chạy React dev server
```powershell
npm run dev
```
- Ứng dụng sẽ chạy ở http://localhost:5173 (hoặc cổng Vite báo)

## 5. Sử dụng
- Truy cập http://localhost:5173 để chat với AI.
- Khi gửi tin nhắn, React sẽ gọi API backend để nhận phản hồi.

## 6. Lưu ý
- Đảm bảo cả backend và frontend đều đang chạy.
- Nếu muốn đổi cổng backend, hãy sửa URL trong file `font-end/src/App.jsx`.
- Đảm bảo file `back-end/app/routers/data.json` tồn tại (nếu chưa có, backend sẽ tự tạo).
- Thư mục `RAG_Document` chứa tài liệu nội bộ cho AI.

## 7. Liên hệ
- Nếu gặp lỗi, kiểm tra log terminal của backend và frontend để biết chi tiết.
