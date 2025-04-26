from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import db
from models import UserCreate, UserLogin, Task
from auth import hash_password, verify_password, create_token, decode_token
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user = await db.users.find_one({"email": payload.get("sub")})
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/register")
async def register(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    await db.users.insert_one({"email": user.email, "password": hashed})
    return {"msg": "User registered"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/tasks")
async def add_task(task: Task, user: dict = Depends(get_current_user)):
    task_data = task.dict()
    task_data["user_id"] = str(user["_id"])
    result = await db.tasks.insert_one(task_data)
    return {"id": str(result.inserted_id)}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, user: dict = Depends(get_current_user)):
    task = await db.tasks.find_one({"_id": ObjectId(task_id), "user_id": str(user["_id"])})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.tasks.delete_one({"_id": ObjectId(task_id)})
    return {"msg": "Task deleted"}

@app.get("/tasks")
async def get_tasks(user: dict = Depends(get_current_user)):
    tasks_cursor = db.tasks.find({"user_id": str(user["_id"])})
    tasks = []
    async for task in tasks_cursor:
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks
