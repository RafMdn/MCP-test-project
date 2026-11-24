from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import asyncio
from langchain_groq import ChatGroq
from uuid import uuid4
from rich import print

load_dotenv()

model = ChatGroq(
    model= "openai/gpt-oss-120b",
    temperature=0,
)

mcp_adapter = MCPAdapter("http://127.0.0.1:8000/mcp")

async def main():
    async with mcp_adapter: 
        tools = await mcp_adapter.list_tools()
        agent = create_agent(
            model= model,
            tools= tools,
            system_prompt="you are a helpful task management assistant",
            checkpointer= InMemorySaver()
        )
        config = {
            "configurable" : {"thread_id" : uuid4()}
        }
        human_question = "can you help me?"

        while human_question != "q":
            result = await agent.ainvoke({"messages" : [HumanMessage(content=human_question)]},
                                         config= config)
            print(result["messages"][-1].content)
            human_question = input("ask another question! ('q' to quit)\n")

if __name__ == "__main__": 
    asyncio.run(main()) 