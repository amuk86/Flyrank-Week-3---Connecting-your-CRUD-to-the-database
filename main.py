import fastapi
import sqlite3

#python -m uvicorn main:app --reload

app = fastapi.FastAPI()

# Stage 0: Database Setup 
conn = sqlite3.connect("task.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    done BOOLEAN
);
""")

tasks = [
    ("Setup FastAPI project", True),
    ("Connect SQLite database", True),
    ("Implement CRUD endpoints", False)
]

# Use IGNORE so re-running the script doesn't crash on UNIQUE constraint errors
conn.executemany(
    "INSERT OR IGNORE INTO tasks (title, done) VALUES (?, ?)",
    tasks
)

conn.commit()
conn.close()

#Helper Function for Database Connections
def get_db():
    conn = sqlite3.connect("task.db")
    # Setting row_factory lets SQLite return dictionary-like rows instead of tuples
    conn.row_factory = sqlite3.Row
    return conn

#Stage 1: GET Route
@app.get("/tasks")
def index():
    db = get_db()
    cursor = db.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    db.close()
    
    # Convert sqlite3.Row objects to standard Python dictionaries so FastAPI returns clean JSON
    return [dict(row) for row in rows]

@app.get("/task_id/{task_id}")
def searchTask(task_id: int):
    db = get_db()
    cursor = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    rows = cursor.fetchall()
    db.close()

    if not rows:
        return {"404": "Task not found"}

    return [dict(row) for row in rows]

#Stage 2: Create new tasks

@app.put("/insert_task")
def putTask(input_title: str, input_done: bool):
    db=get_db()
    cursor = db.execute("INSERT OR IGNORE INTO tasks (title, done) VALUES (?, ?)",(input_title,input_done,))
    db.commit()
    db.close()
    if not input_title:
        return 400
    return 201

#Stage 3 — Update and delete 
@app.delete("/removeTask")
def removeTask(id: int):
    db = get_db()
    cursor = db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    return f"row with id:{id} deleted"
