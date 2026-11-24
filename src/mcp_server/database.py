import sqlite3
from pathlib import Path
from rich import print

project_root = Path(__file__).resolve().parents[2]
data_dir = project_root / "data"
db_path = data_dir / "tasks.db"

def init_db() -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'todo',
                priority TEXT NOT NULL DEFAULT 'medium',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    finally:
        conn.close()


def save_task(task : dict) -> int:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try : 
        cursor.execute("""
        INSERT INTO tasks(
            title, description, priority, status
        )
        VALUES(?,?,?,?)
        """,
            (
                task["title"],
                task["description"],
                task["priority"],
                task["status"],
            )
        )
        task_id = cursor.lastrowid
        conn.commit()
    finally:
        conn.close()
    return task_id

def update_task_status(task_id : int , status : str) -> dict:
    VALID_STATUSES = {"todo", "in_progress", "done"}

    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try : 
        cursor.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE task_id = ?
            """,
            (status , task_id)
        )
        conn.commit()
        record = cursor.execute(
            """
            SELECT * FROM tasks
            WHERE task_id = ?
            """, (task_id,)
        ).fetchone()

    finally:
        conn.close()
    if record is None:
        return {"error" : f"the task_id : {task_id} does not exist"}
    return dict(record)

def get_all_tasks() -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try : 
        cur.execute("SELECT * from tasks;")
        rows = cur.fetchall()
    finally:
        conn.close()

    return [dict(row) for row in rows]

if __name__ == "__main__":
    print(get_all_tasks())
    # update_task_status(
    #     task_id= 1,
    #     status= "in_progress"
    # )
    # save_task({
    #     "title" : "task1",
    #     "description" : "the first task",
    #     "priority" : "low",
    #     "status" : "todo"
    # })
