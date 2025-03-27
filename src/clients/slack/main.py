import asyncio
from contextlib import asynccontextmanager
from logging import Logger

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler


from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

from clients.settings import logger, PYTHONPATH, SLACK_BOT_TOKEN, SLACK_APP_TOKEN
from clients.slack.prompts import MCP_CLIENT_SYSTEM_PROMPT

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
    mcp_servers=mcp_servers
)
slack = AsyncApp(token=SLACK_BOT_TOKEN, logger=logger)


@slack.event("assistant_thread_started")
async def handle_assistant_thread_started_events(say):
    say(f"Hello, I am an CMP Agent. I am running {len(mcp_servers)} servers now")


# @app.event("app_mention")
@slack.event("message")
async def handle_mention(event: dict, say, ack, set_status, logger: Logger):
    user = event['user']
    text = event['text']
    query = text.split(">", 1)[1].strip() if ">" in text else text

    await ack()
    await set_status(f"Working on your request: '{query}'...")

    try:
        result = await agent.run(query)
        await say(f"<@{user}> {result.data}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await say(f"Sorry <@{user}>, I encountered an error.")


@asynccontextmanager
async def shared_mcp_servers():
    async with agent.run_mcp_servers():
        logger.info("MCP servers started")
        yield
        logger.info("MCP servers stopping")


async def main():
    handler = AsyncSocketModeHandler(slack, SLACK_APP_TOKEN)
    async with shared_mcp_servers():
        await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
