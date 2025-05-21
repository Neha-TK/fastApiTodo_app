# 📝 FastAPI Todo App with PostgreSQL

This is a beginner-friendly **Todo App** backend built using **FastAPI**, **PostgreSQL**, and **SQLModel**.

---

## 📊 API Endpoints

| Method | Endpoint              | Description                     | Auth Required |
| ------ | --------------------- | ------------------------------- | ------------- |
| POST   | `/signup`             | Register a new user             | ❌             |
| POST   | `/login`              | Login and get JWT token         | ❌             |
| POST   | `/todos`              | Create a new todo               | ✅             |
| GET    | `/todos`              | Get all todos grouped by status | ✅             |
| PUT    | `/todos/{todo_id}`    | Edit a todo                     | ✅             |
| PATCH  | `/todos/{todo_id}/complete` | Mark todo as completed   | ✅             |
| DELETE | `/todos/{todo_id}`    | Delete a todo                   | ✅             |

---

## ✅ Quickstart Guide

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/fastapi-todo.git
cd fastapi-todo
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Use 'source venv/bin/activate' on Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

- Ensure PostgreSQL is running
- Create a database: `todo_db`
- Fill in your `.env` file (you can copy from `.env.sample`):

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/todo_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the App

```bash
python run.py
```

### 6. Visit Swagger UI

Open in your browser:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Use the **Authorize** button in Swagger UI to input the JWT token.

---

## 📁 Project Structure

```
todo_app/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   ├── schemas.py
│   │   ├── routes.py
│   │   └── endpoints/
│   │       ├── common.py
│   │       └── todos.py
│   ├── db/
│   │   ├── engine.py
│   │   └── models.py
│   ├── helper/
│   │   └── auth.py
│   └── main.py
├── run.py
├── .env
├── .env.sample
├── requirements.txt
├── README.md
└── .gitignore
```

