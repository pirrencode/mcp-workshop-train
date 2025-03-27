# MCP Workshop

## Introduction

This code repo contains workshop materials for Model Context Protocol by Anthropic

## Directory Structure

```text
./
├── docker-compose.yaml            # Docker compose file
├── Dockerfile                     # Dockerfile
├── poetry.lock                    # Poetry lock file
├── pyproject.toml                 # Poetry project configuration file
├── README.md                      # This file
└── src
    ├── clients                    # MCP Clients code
    │   ├── pydantic_ai            # MCP  Client app with Pydantic AI and AWS Bedrock model (Requires AWS credentials)
    │   │   ├── __init__.py
    │   │   ├── main.py            # app code
    │   │   └── prompts.py         # LLM prompts
    │   ├── settings               # app configs
    │   │   ├── __init__.py
    │   │   └── main.py
    │   └── slack                  # MCP Client with Slack Bolt app (requires Slack API token)
    │       ├── __init__.py
    │       ├── main.py            # app code
    │       ├── manifest.yaml      # slack app manifest file
    │       └── prompts.py         # LLM prompts
    └── servers                    # MCP Servers code
        ├── download               # Download HTML page MCP Server
        │   ├── __init__.py
        │   ├── main.py
        │   └── utils.py
        ├── online_search          # MCP Server for Google Programmable Search (requires API key)
        │   ├── __init__.py
        │   └── main.py            # app code
        ├── settings               # app configs
        │   ├── __init__.py
        │   └── main.py
        └── today                  # MCP Server Returns today's date in various formats. Used to help LLM to calculate dates in relations to curreen date
            ├── __init__.py
            └── main.py             # app code
```

## MCP Servers

### Download

This server downloads the HTML content of a given URL. It uses the `httpx` library to download the content.

Then it converts the HTML content to Markdown text. So it is easier for LLM to read and understand the content.

### Online Search

This server uses the Google Programmable Search API to search the web for a given query. It requires an API key to be set in the environment variable `GOOGLE_API_KEY` and `GOOGLE_SEARCH_ENGINE_ID`

See [Google Programmable Search API](https://developers.google.com/custom-search/v1/overview) for more information.

### Today

This server returns today's date in various formats. It is used to help LLM calculate dates in relation to the current date.

For instance it will help LLM to answer about `What happened at the last Tuesday?`

## MCP Clients

### Pydantic AI

This MCP client uses the Pydantic AI model from AWS Bedrock. It requires AWS credentials to be set in the environment variables.

This is not interactive client, it loads the model and does one task to present in STDOUT.

By default it is using Claude 3.7 model from AWS Bedrock.

### Slack

This MCP client extends the Pydantic AI client to work with Slack. It uses the Slack Bolt library to create a Slack app.

It requires a Slack API token to be set in the environment variable `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`. You can create a Slack app and get the tokens from the Slack API using the manifest file `src/clients/slack/manifest.yaml`

## Running the code

TBD
