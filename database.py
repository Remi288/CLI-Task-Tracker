import sqlite3
from typing import List
import datetime
from model import Todo


conn = sqlite3.connect("todo.db")
c = conn.cursor()


def create_table():
    c.execute(
        """CREATE TABLE IF NOT EXISTS todo (
        task TEXT,
        category TEXT,
        date_added TEXT,
        date_completed TEXT,
        status INTEGER,
        position INTEGER)"""
    )


create_table()


def add_todo(todo: Todo):
    c.execute("SELECT count(*) FROM todo")
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute(
            "INSERT INTO todo VALUES (:task, :category, :date_added, :date_completed, :status, :position)",
            {
                "task": todo.task,
                "category": todo.category,
                "date_added": todo.date_added,
                "date_completed": todo.date_completed,
                "status": todo.status,
                "position": todo.position,
            },
        )


def get_all_todos() -> List[Todo]:
    c.execute("SELECT * FROM todo")
    result = c.fetchall()
    todos = []
    for row in result:
        todos.append(Todo(*row))
    return todos


def delete_todo(position: int):
    c.execute('SELECT count(*) FROM todo')
    count = c.fetchone()[0]
    with conn:
        c.execute("DELETE FROM todo WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_postion(pos, pos-1, False)


def change_postion(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE todo SET position=:new_position WHERE position=:old_position', {'old_position': old_position, 'new_position': new_position})
    if commit:
        conn.commit()


def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
              c.execute("UPDATE todo SET task=:task, category=:category WHERE position=:position", {'task': task, 'category': category, 'position': position})
        elif task is not None:
                c.execute("UPDATE todo SET task=:task WHERE position=:position", {'task': task, 'position': position})
        elif category is not None:
                c.execute("UPDATE todo SET category=:category WHERE position=:position", {'category': category, 'position': position})

def complete_todo(position: int):
    with conn:
        c.execute("UPDATE todo SET status=2, date_completed=:date_completed WHERE position=:position", {'date_completed': datetime.datetime.now().isoformat(), 'position': position})
