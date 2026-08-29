import fastapi
import sqlite3

#python -m uvicorn main:app --reload

app = fastapi.FastAPI()

# --- Stage 0: Database Setup ---
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