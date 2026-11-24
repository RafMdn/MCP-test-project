from typing import Literal
from uuid import uuid4

from fastmcp import FastMCP
from database import (
    get_all_tasks,
    save_task,
    update_task_status
)

mcp = FastMCP("MCP SERVER")

@mcp.tool(name="create task", description="this tool is used to create new tasks")
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


# @mcp.tool()

# @mcp.tool()

if __name__ == "__main__":
    mcp.run(transport="http", port=8000) 
    create_task(title="task2", description="this is the second task")