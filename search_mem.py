from mem0 import MemoryClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

username = os.getenv("REDDIT_USERNAME")
query = "What do you know about me?"
filters = {
   "OR": [
      {"user_id": f"reddit_analyst_{username}"},
   ]
}

results = client.search(query, version="v2", filters=filters)
print(results)