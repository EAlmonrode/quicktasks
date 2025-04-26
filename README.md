# QuickTasks 📝

Simple Task Manager built with FastAPI + MongoDB + HTML/CSS Frontend.

## Features
- User Registration and Login (with JWT Authentication)
- Add Tasks
- View Tasks
- Delete Tasks
- MongoDB Atlas for database
- Frontend styled with basic CSS

## How to Run
1. Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```

2. Start FastAPI server:
    ```bash
    uvicorn backend.main:app --reload
    ```

3. Open `frontend/index.html` in your browser.

## Tech Stack
- FastAPI
- MongoDB (Atlas)
- Motor (MongoDB async driver)
- Passlib (Password hashing)
- Python-Jose (JWT Tokens)
- HTML/CSS

---

Built with ❤️ by [Your Name]
