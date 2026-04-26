from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from pathlib import Path
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

DATA_FILE = Path(__file__).parent / "backend" / "data" / "tasks.json"

def load_tasks() -> List[dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks: List[dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None

@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/api/tasks")
def get_tasks(view: str = "active"):
    tasks = load_tasks()
    
    if view == "active":
        return [t for t in tasks if t.get("status") == "active" and not t.get("deleted")]
    elif view == "done":
        return [t for t in tasks if t.get("status") == "done" and not t.get("deleted")]
    elif view == "trash":
        return [t for t in tasks if t.get("deleted")]
    return []

@app.post("/api/tasks")
def create_task(task: TaskCreate):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    
    new_task = {
        "id": new_id,
        "title": task.title,
        "status": "active",
        "deleted": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            if data.title is not None:
                task["title"] = data.title
            if data.status is not None:
                task["status"] = data.status
            save_tasks(tasks)
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["deleted"] = True
            save_tasks(tasks)
            return {"ok": True}
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/api/tasks/{task_id}/restore")
def restore_task(task_id: int):
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["deleted"] = False
            save_tasks(tasks)
            return {"ok": True}
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}/permanent")
def permanent_delete(task_id: int):
    tasks = load_tasks()
    
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)