# Task API — FastAPI + SQLite

A simple task management API built with FastAPI and SQLite, supporting listing, searching, creating, and deleting tasks.

## Why SQLite Was Chosen

SQLite was chosen for this project because:

- **Zero configuration** — it's a serverless, file-based database with no separate database server to install, configure, or run. This makes the project easy for anyone to clone and start immediately.
- **Built into Python** — the `sqlite3` module is part of the Python standard library, so no extra dependencies are needed to talk to the database.
- **Perfect for small/prototype apps** — for a lightweight task list with modest read/write volume, SQLite's performance and reliability are more than sufficient.
- **Portable** — the entire database lives in a single file that can be copied, backed up, or version-controlled independently of any server process.
- **Self-creating schema** — since SQLite just reads/writes a local file, the app can automatically create the database and its tables on startup (see Checkpoint below), so there's no manual setup step for new contributors.

## Where the Database File Is Stored

The database is stored as a single file named **`task.db`** in the **root directory of the project** (the same folder as `main.py`). It is created automatically the first time the app is run, via:

```python
conn = sqlite3.connect("task.db")
```

> **Note:** `task.db` should be added to `.gitignore` so the actual database file isn't committed to version control — only the code that generates it is.

## How to Start the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/amuk86/Flyrank-Week-3---Connecting-your-CRUD-to-the-database
   cd <your-repo-folder>
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

4. **Run the app**
   ```bash
   python -m uvicorn main:app --reload
   ```

   On startup, the app automatically:
   - Connects to (and creates, if missing) `task.db`
   - Creates the `tasks` table if it doesn't already exist
   - Seeds the table with a few sample tasks (using `INSERT OR IGNORE`, so re-running the app won't duplicate data or crash on the `UNIQUE` constraint)

5. **Open the interactive API docs**

   Once running, visit:
   ```
   http://127.0.0.1:8000/docs
   ```

## API Endpoints

| Method | Endpoint                | Description                       |
|--------|--------------------------|------------------------------------|
| GET    | `/tasks`                 | List all tasks                    |
| GET    | `/task_id/{task_id}`     | Get a single task by ID           |
| PUT    | `/insert_task`           | Create a new task                 |
| DELETE | `/removeTask`            | Delete a task by ID                |

## Database Viewer Screenshot

<img width="1366" height="768" alt="Screenshot From 2026-08-29 18-21-09" src="https://github.com/user-attachments/assets/6ff86897-fa9b-4903-bbec-25958a90505e" />

```

## Example SQL Query Executed

```sql
SELECT * FROM tasks WHERE id = 1;
```

This query was run against `task.db` (via the `/task_id/{task_id}` endpoint) to retrieve a single task by its primary key. Example result:

| id | title                    | done |
|----|---------------------------|------|
| 1  | Setup FastAPI project     | 1    |

## Checkpoint ✅

Someone cloning this repository can run the project with a single command (`python -m uvicorn main:app --reload`) and the SQLite database (`task.db`) — along with the `tasks` table and seed data — is created automatically. No manual database setup is required.
