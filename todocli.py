import typer
from rich.console import Console
from rich.table import Table

from helper import get_category_color
from model import Todo
from database import add_todo, get_all_todos, delete_todo, complete_todo, update_todo


console = Console()

app = typer.Typer()

@app.command(short_help='adds an item to the todo list')
def add(task: str, category:str):
    """Adds an item to the todo list"""
    typer.echo(f'Adding {task} to {category}')
    todo = Todo(task, category)
    add_todo(todo)
    show()

@app.command(short_help='removes an item from the todo list')
def delete(postion:int):
    """Removes an item from the todo list"""
    typer.echo(f'Deleting item {postion}')
    delete_todo(postion-1)
    show()

@app.command(short_help='update items in the todo list')
def update(postion:int, task:str = None, category:str = None):
    """Updates an item in the todo list"""
    typer.echo(f'Updating item {postion}')
    update_todo(postion-1, task, category)
    show()

@app.command(short_help='complete an item in the todo list')
def complete(postion:int):
    """Completes an item in the todo list"""
    typer.echo(f'Completing item {postion}')
    complete_todo(postion-1)
    show()

@app.command(short_help='list all items in the todo list')
def show():
    """Lists all items in the todo list"""
    tasks = get_all_todos()
    console.print("[bold magenta]Todos!:[/bold magenta]", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Status", min_width=12, justify="right")
    for i, task in enumerate(tasks, start=1):
        color = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(str(i), task.task, f'[{color}]{task.category}[/{color}]', is_done_str)
    console.print(table)


if __name__ == '__main__':
    app()
