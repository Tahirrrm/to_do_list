import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DATA_FILE = "backend/data/tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open("frontend/index.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path.startswith("/static/"):
            path = self.path[1:].replace("static/", "frontend/")
            if os.path.exists(path):
                self.send_response(200)
                ext = path.split(".")[-1]
                ctype = {"js": "application/javascript", "css": "text/css", "png": "image/png"}.get(ext, "text/plain")
                self.send_header("Content-Type", f"{ctype}; charset=utf-8")
                self.end_headers()
                with open(path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        elif self.path == "/api/tasks":
            params = parse_qs(urlparse(self.path).query)
            view = params.get("view", ["active"])[0]
            tasks = load_tasks()
            
            if view == "active":
                result = [t for t in tasks if t.get("status") == "active" and not t.get("deleted")]
            elif view == "done":
                result = [t for t in tasks if t.get("status") == "done" and not t.get("deleted")]
            elif view == "trash":
                result = [t for t in tasks if t.get("deleted")]
            else:
                result = []
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        
        if self.path == "/api/tasks":
            data = json.loads(body)
            tasks = load_tasks()
            new_id = max([t["id"] for t in tasks], default=0) + 1
            new_task = {"id": new_id, "title": data["title"], "status": "active", "deleted": False}
            tasks.append(new_task)
            save_tasks(tasks)
            
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(new_task).encode("utf-8"))
        
        elif "/restore" in self.path:
            path_parts = self.path.split("/")
            task_id = int(path_parts[2])
            tasks = load_tasks()
            for t in tasks:
                if t["id"] == task_id:
                    t["deleted"] = False
            save_tasks(tasks)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        
        else:
            self.send_error(404)

    def do_PATCH(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        
        if "/api/tasks/" in self.path:
            path_parts = self.path.split("/")
            task_id = int(path_parts[3])
            data = json.loads(body)
            tasks = load_tasks()
            
            for t in tasks:
                if t["id"] == task_id:
                    if "title" in data:
                        t["title"] = data["title"]
                    if "status" in data:
                        t["status"] = data["status"]
            save_tasks(tasks)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        else:
            self.send_error(404)

    def do_DELETE(self):
        if "/api/tasks/" in self.path and "/permanent" not in self.path:
            path_parts = self.path.split("/")
            task_id = int(path_parts[3])
            tasks = load_tasks()
            
            for t in tasks:
                if t["id"] == task_id:
                    t["deleted"] = True
            save_tasks(tasks)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        
        elif "/permanent" in self.path:
            path_parts = self.path.split("/")
            task_id = int(path_parts[2])
            tasks = load_tasks()
            tasks = [t for t in tasks if t["id"] != task_id]
            save_tasks(tasks)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass

print("ToDo List: http://localhost:3000")
server = HTTPServer(("127.0.0.1", 3000), Handler)
server.serve_forever()