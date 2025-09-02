# Reddit Analysis with CrewAI, MCP, and Mem0

## Overview
This project provides a framework for analyzing Reddit posts and engagement patterns using CrewAI agents, the MCPServerAdapter for tool integration, and Mem0 for persistent memory. It enables:
- Fetching and analyzing Reddit posts
- Storing and searching analysis insights
- Leveraging historical memory for improved recommendations

## Features
- **Reddit Data Fetcher**: Fetches subreddit posts and details using MCP tools
- **Memory-Enhanced Analysis**: Stores and retrieves insights using Mem0
- **Automated Pattern Discovery**: Identifies engagement patterns and trends

## Directory Structure
- `client.py`: Example of using CrewAI with MCP tools to fetch Reddit data
- `reddit_agent_memory.py`: Advanced agent with memory for analysis and recommendations
- `search_mem.py`: Script to search stored memories
- `delete_mem.py`: Script to delete all memories for a user

## Setup & Installation
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd reddit
   ```
2. **Install dependencies**
   Ensure you have Python 3.9+ (recommended: 3.12). Install required packages:
   ```bash
   pip install crewai crewai_tools mcp mem0 python-dotenv
   ```
3. **Environment Variables**
   Create a `.env` file in the project root with the following variables:
   ```env
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USERNAME=your_reddit_username
   REDDIT_REFRESH_TOKEN=your_reddit_refresh_token
   REDDIT_USER_AGENT=your_user_agent
   OPENAI_API_KEY=your_openai_api_key
   MEM0_API_KEY=your_mem0_api_key
   ```

## Usage
### 1. Fetch Reddit Data
Run the basic client to fetch hot posts from a subreddit:
```bash
python client.py
```

### 2. Memory-Enhanced Reddit Analysis
Run the advanced agent with memory and analysis capabilities:
```bash
python reddit_agent_memory.py
```

### 3. Search Memories
Query stored memories for insights:
```bash
python search_mem.py
```

### 4. Delete All Memories for User
Remove all stored memories for the configured Reddit user:
```bash
python delete_mem.py
```

## Environment Variables
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_REFRESH_TOKEN`, `REDDIT_USER_AGENT`: Reddit API credentials
- `OPENAI_API_KEY`: OpenAI API key for LLM
- `MEM0_API_KEY`: Mem0 API key for memory storage

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

## Contact
For questions or support, open an issue or contact the maintainer.
