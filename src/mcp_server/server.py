from typing import Literal
from uuid import uuid4

from fastmcp import FastMCP
from database import (
    get_all_tasks,
    save_task,
    update_task_status as db_update_task_status
)

mcp = FastMCP("MCP SERVER")

@mcp.tool(name="create_task", description="this tool is used to create new tasks")
def create_task(title: str, priority:str = "medium", description:str = "") -> dict:
    """
    This function creates new task is our database
    """
    status = "todo"
    task = {
        "title" : title,
        "description" : description,
        "status" : status,
        "priority" : priority
        }
    
    save_task(task=task)

    return task


@mcp.tool(name="list_tasks" , description="This tool provides all the names of the tasks present in the database")
def list_task() ->list[dict]:
    """This tool provides all the names of the tasks present in the database"""
    return get_all_tasks()

@mcp.tool(name="update_task_status", description="This tool will update the status of a given task indentified with it's task_id arguement")
def update_task_status(task_id : int , status : Literal["todo", "in_progress" , "done"])->dict:
    """This tool will update the status of a given task indentified with it's task_id arguement"""
    return db_update_task_status(task_id=task_id, status=status)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000) 
    create_task(title="task2", description="this is the second task")