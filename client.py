from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

import os
import warnings
from pydantic import PydanticDeprecatedSince20

# Suppress Pydantic v2 deprecation warnings
warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

# Define how to start your Reddit MCP server
server_params = StdioServerParameters(
    command="python3",
    args=["Reddit MCP/src/mcp_reddit/reddit_fetcher.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

# Connect to MCP server tools
with MCPServerAdapter(server_params) as tools:
    print(f"✅ Available tools: {[tool.name for tool in tools]}")

    # Define an agent that can use those tools
    reddit_agent = Agent(
        role="Reddit Data Fetcher",
        goal="Fetch subreddit posts and post details",
        backstory=(
            "You are a Reddit expert. "
            "You help users explore hot posts and detailed content from subreddits."
        ),
        tools=tools,   # <- important: attach the MCP tools here
        verbose=True,
    )

    # Define a sample task using MCP tools
    task = Task(
        description="Fetch the top 5 hot posts from r/Python",
        agent=reddit_agent,
    )

    # Run the crew with a single agent and task
    crew = Crew(
        agents=[reddit_agent],
        tasks=[task],
        verbose=True,
    )

    result = crew.run()
    print("\n🔎 Task Result:\n", result)
