from mem0 import MemoryClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

# Delete all memories for a specific user
username = os.getenv("REDDIT_USERNAME")
client.delete_all(user_id=f"reddit_analyst_{username}")