import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

from clients.settings import logger, PYTHONPATH
from clients.pydantic_ai.prompts import MCP_CLIENT_SYSTEM_PROMPT

# For SSE
# MCPServerHTTP('http://localhost:3000/sse')
mcp_servers = [
    MCPServerStdio(**kwargs)
    for kwargs in [
        {
            "command": "mcp",
            "args": ["run", "src/servers/today/main.py"],
            "env": {"PYTHONPATH": PYTHONPATH},
        },
        {
            "command": "mcp",
            "args": ["run", "src/servers/download/main.py"],
            "env": {"PYTHONPATH": PYTHONPATH},
        },
        {
            "command": "mcp",
            "args": ["run", "src/servers/online_search/main.py"],
            "env": {"PYTHONPATH": PYTHONPATH},
        },
    ]
]

agent = Agent(
    model='bedrock:us.anthropic.claude-3-7-sonnet-20250219-v1:0',
    system_prompt=MCP_CLIENT_SYSTEM_PROMPT,
    mcp_servers=mcp_servers,
)

async def main():
    question = 'Search for Model Context Protocol meetup and give me a breath summary'
    async with agent.run_mcp_servers():
        result = await agent.run(question)
    logger.info(result.data)

if __name__ == "__main__":
    asyncio.run(main())
