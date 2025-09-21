# ChatBot based on ReACT

## Giới thiệu dự án

Đây là dự án ChatBot sử dụng mô hình ReACT kết hợp với RAG (Retrieval-Augmented Generation) để cung cấp khả năng trò chuyện thông minh, hỗ trợ truy xuất dữ liệu và quản lý người dùng. Dự án được xây dựng trên nền tảng FastAPI, dễ dàng mở rộng và tích hợp với các hệ thống khác.

## Công nghệ sử dụng
- FastAPI
- Uvicorn
- LangChain
- MongoDB
- PyJWT
- Pydantic
- Passlib
- Các thư viện AI: langchain_huggingface, sentence_transformers, langchain-google-genai

## Hướng dẫn cài đặt và chạy dự án

1. **Clone dự án**

```bash
# Clone về máy
https://github.com/bexanhtuoi/ChatBot-based-on-ReACT.git
```

2. **Cài đặt các thư viện cần thiết**

```bash
cd Server
pip install -r requirements.txt
```

3. **Chạy server FastAPI**

```bash
uvicorn app.main:app --reload
```

Server sẽ chạy tại địa chỉ: `http://127.0.0.1:8000`

## Chi tiết các endpoint

### 1. Auth (Xác thực)
- `POST /auth/register`: Đăng ký tài khoản mới
  - Body: `{ email, password, ... }`
  - Trả về: `{ message }`
- `POST /auth/token`: Đăng nhập, trả về access token
  - Body: `username`, `password` (dùng OAuth2PasswordRequestForm)
  - Trả về: `{ message }` và cookie access_token
- `POST /auth/logout`: Đăng xuất, xóa access_token
  - Trả về: `{ message }`

### 2. Users (Người dùng)
- `GET /users/all`: Lấy danh sách tất cả người dùng (có phân trang)
- `GET /users/{user_id}`: Lấy thông tin người dùng theo ID
- `GET /users/e/{email}`: Lấy thông tin người dùng theo email
- `DELETE /users/{user_id}`: Xóa người dùng (chỉ chính chủ)
- `PUT /users/{user_id}`: Cập nhật thông tin người dùng (chỉ chính chủ)

### 3. Chats (Trò chuyện)
- `GET /chats/all`: Lấy danh sách các cuộc trò chuyện công khai (có phân trang)
- `GET /chats/{chat_id}`: Lấy thông tin cuộc trò chuyện theo ID
- `GET /chats/u/{user_id}`: Lấy các cuộc trò chuyện của một user (chỉ chính chủ)
- `DELETE /chats/{chat_id}`: Xóa cuộc trò chuyện (chỉ chính chủ)
- `POST /chats/`: Gửi tin nhắn mới, tạo hoặc cập nhật cuộc trò chuyện
  - Body: `{ message, ... }`
  - Trả về: `{ message, response }`
- `PUT /chats/{chat_id}`: Cập nhật thuộc tính cuộc trò chuyện (chỉ chính chủ)

## Liên hệ
- Tác giả: bexanhtuoi
- Github: https://github.com/bexanhtuoi/ChatBot-based-on-ReACT
