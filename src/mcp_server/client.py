from fastmcp import Client
import asyncio
from rich import print

client = Client("http://127.0.0.1:8000/mcp")

async def get_all_tools():
    async with client:
        tools = await client.list_tools()
    return tools

async def create_task_using_mcp():
    async with client:
        result = await client.call_tool(
            "create_task",
            {
                "title": "task2", 
                "priority":"high", 
                "description": "This is the second task"
            }
        )
        print(result.data)

    return result.data

async def update_task_status_using_mcp(task_id : int , status: str):
    async with client:
        result = await client.call_tool(
            "update_task_status",
            {
             "task_id" : task_id,
             "status" : status   
            }
        )
        print(result.data)
    return result
if __name__ == "__main__":
    # asyncio.run(get_all_tools())
    asyncio.run(update_task_status_using_mcp(task_id=2, status="in_progress"))


    # asyncio.run(create_task_using_mcp())
