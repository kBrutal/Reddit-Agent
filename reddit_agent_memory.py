import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from mem0 import MemoryClient
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Mem0 client
memory_client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

# Configure MCP server parameters for Reddit
server_params = StdioServerParameters(
    command="uvx",
    args=["--from", "git+https://github.com/kBrutal/Reddit-MCP.git", "mcp-reddit"],
    env={
        "REDDIT_CLIENT_ID": os.getenv('REDDIT_CLIENT_ID'),
        "REDDIT_CLIENT_SECRET": os.getenv('REDDIT_CLIENT_SECRET'),
        "REDDIT_USERNAME": os.getenv('REDDIT_USERNAME'),
        "REDDIT_REFRESH_TOKEN": os.getenv('REDDIT_REFRESH_TOKEN'),
        "REDDIT_USER_AGENT": os.getenv('REDDIT_USER_AGENT'),
    }
)

# Explicitly set the LLM (OpenAI model)
openai_llm = LLM(
    model="openai/gpt-5-mini",  # You can change to "gpt-4", "gpt-3.5-turbo", etc.
    api_key=os.getenv("OPENAI_API_KEY"),
    drop_params=True,
    additional_drop_params=["stop", "temperature"]
)
openai_api_key = os.getenv("OPENAI_API_KEY")

class RedditMemoryManager:
    """Manages memory operations for Reddit analysis using Mem0"""
    
    def __init__(self, memory_client, user_id):
        self.memory_client = memory_client
        self.user_id = user_id
    
    def store_post_analysis(self, post_data, engagement_metrics, insights):
        """Store analysis of a specific post"""
        memory_data = {
            "type": "post_analysis",
            "post_data": post_data,
            "engagement_metrics": engagement_metrics,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }
        
        # Create a structured memory entry
        memory_text = f"""
        Reddit Post Analysis:
        - Title: {post_data.get('title', 'N/A')}
        - Subreddit: {post_data.get('subreddit', 'N/A')}
        - Upvotes: {engagement_metrics.get('upvotes', 0)}
        - Comments: {engagement_metrics.get('comments', 0)}
        - Key Insights: {insights}
        - Posted on: {post_data.get('created_utc', 'N/A')}
        """
        
        try:
            self.memory_client.add(
                messages=[{"role": "user", "content": memory_text}],
                user_id=self.user_id,
                metadata=memory_data
            )
            print(f"✅ Stored memory for post: {post_data.get('title', 'Unknown')[:50]}...")
        except Exception as e:
            print(f"❌ Error storing post memory: {e}")
    
    def store_engagement_pattern(self, pattern_type, pattern_details):
        """Store identified engagement patterns"""
        memory_text = f"""
        Engagement Pattern Discovered:
        - Pattern Type: {pattern_type}
        - Details: {pattern_details}
        - Discovery Date: {datetime.now().strftime('%Y-%m-%d')}
        """
        
        try:
            self.memory_client.add(
                messages=[{"role": "user", "content": memory_text}],
                user_id=self.user_id,
                metadata={
                    "type": "engagement_pattern",
                    "pattern_type": pattern_type,
                    "details": pattern_details,
                    "timestamp": datetime.now().isoformat()
                }
            )
            print(f"✅ Stored engagement pattern: {pattern_type}")
        except Exception as e:
            print(f"❌ Error storing pattern memory: {e}")
    
    def get_relevant_memories(self, query):
        """Retrieve relevant memories based on query"""
        try:
            memories = self.memory_client.search(
                query=query,
                user_id=self.user_id,
                limit=10
            )
            return memories
        except Exception as e:
            print(f"❌ Error retrieving memories: {e}")
            return []
    
    def get_historical_insights(self):
        """Get all historical insights for context"""
        try:
            all_memories = self.memory_client.get_all(user_id=self.user_id)
            return all_memories
        except Exception as e:
            print(f"❌ Error retrieving historical insights: {e}")
            return []

def create_memory_enhanced_agent(reddit_tools, memory_manager):
    """Create a Reddit analyst agent enhanced with memory capabilities"""
    
    # Get historical insights to inform the agent
    historical_memories = memory_manager.get_historical_insights()
    memory_context = ""
    
    if historical_memories:
        print(f"📚 Found {len(historical_memories)} historical insights")
        memory_context = "\n\nHISTORICAL INSIGHTS FROM PREVIOUS ANALYSES:\n"
        for memory in historical_memories[:5]:  # Use last 5 insights
            memory_context += f"- {memory.get('memory', '')}\n"
    else:
        print("📚 No historical insights found - starting fresh")
    
    backstory = f"""Expert at analyzing social media data and identifying patterns that lead to viral content. 
    You have access to historical analysis data that helps inform your recommendations.{memory_context}
    
    IMPORTANT: After analyzing posts, you should identify and extract:
    1. Successful post characteristics (titles, timing, topics)
    2. Engagement patterns (what gets upvotes vs comments)
    3. Subreddit-specific trends
    4. Content formats that work best
    
    Use this information along with historical insights to make data-driven recommendations."""
    
    return Agent(
        role="Reddit Post Analyst with Memory",
        goal="Analyze Reddit posting patterns using historical insights to identify what drives engagement. Suggest optimal next reddit posts based on learned patterns. Boil down to a single post after making all the analysis",
        backstory=backstory,
        tools=reddit_tools,
        verbose=True,
        reasoning=True,
        llm=openai_llm
    )

def extract_and_store_insights(analysis_result, memory_manager):
    """Extract insights from analysis result and store them in memory"""
    
    
    try:
        # Store the general analysis as a memory
        memory_manager.memory_client.add(
            messages=[{"role": "assistant", "content": str(analysis_result)}],
            user_id=memory_manager.user_id,
            metadata={
                "type": "analysis_result",
                "timestamp": datetime.now().isoformat(),
                "analysis_type": "reddit_engagement_analysis"
            }
        )
        print("✅ Stored analysis result in memory")
        

        if "high engagement" in str(analysis_result).lower():
            memory_manager.store_engagement_pattern(
                "high_engagement_indicators",
                "Analysis identified specific characteristics that lead to high engagement"
            )
        
    except Exception as e:
        print(f"❌ Error storing analysis insights: {e}")

# Test the connection and create your first agent with memory
try:
    # Initialize memory manager
    username = os.getenv('REDDIT_USERNAME')
    memory_manager = RedditMemoryManager(memory_client, user_id=f"reddit_analyst_{username}")
    
    with MCPServerAdapter(server_params) as reddit_tools:
        print(f"Available Reddit tools: {[tool.name for tool in reddit_tools]}")

        # Create Reddit Data Analyst Agent with memory enhancement
        reddit_analyst = create_memory_enhanced_agent(reddit_tools, memory_manager)

        # Create analysis task with memory context
        relevant_memories = memory_manager.get_relevant_memories("reddit engagement patterns topic")
        
        memory_context_for_task = ""
        if relevant_memories:
            memory_context_for_task = "\n\nRELEVANT HISTORICAL INSIGHTS:\n"
            for memory in relevant_memories[:3]:  # Top 3 most relevant
                memory_context_for_task += f"- {memory.get('memory', '')}\n"

        username = os.getenv('REDDIT_USERNAME')
        analysis_task = Task(
            description=f"""Analyze recent Reddit posts on hot topics related to topics {username} is interested in to identify engagement patterns. 
            Use both current data and historical insights to suggest new topics and subreddits for posts.
            
            {memory_context_for_task}
            
            Provide:
            1. Analysis of current trending topics {username} is interested
            2. Engagement pattern analysis based on upvotes, comments, and timing
            3. Specific post suggestions with complete Title and Body content
            4. Recommended subreddits and optimal posting times
            5. Key insights that should be remembered for future analysis
            
            If no post found in reddit for the user, fetch hot posts from most common subreddits.
            Focus on actionable recommendations based on data patterns.""",
            expected_output="A comprehensive analysis with specific post recommendations, including complete title and body content, plus insights to remember for future use. A post made based on this analysis which can give engagement.",
            agent=reddit_analyst
        )

        # Create and run the crew
        reddit_crew = Crew(
            agents=[reddit_analyst],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )

        print("Starting Reddit post analysis with memory enhancement...")
        result = reddit_crew.kickoff()
        
        # Store the insights from this analysis
        extract_and_store_insights(result, memory_manager)
        
        print("\nAnalysis Complete!")
        print(result)
        
        # Store any specific successful patterns identified in this run
        # (You can customize this based on what patterns you want to track)
        if hasattr(result, 'raw') and result.raw:
            memory_manager.store_engagement_pattern(
                "latest_analysis_insights",
                f"Latest analysis completed on {datetime.now().strftime('%Y-%m-%d')} with new insights about topic"
            )

except Exception as e:
    print(f"Error: {e}")
    print("Make sure your Reddit credentials, OpenAI API key, and Mem0 API key are correct and the MCP server is working")

# Optional: Print memory statistics
try:
    if 'memory_manager' in locals():
        all_memories = memory_manager.get_historical_insights()
        print(f"\n📊 Memory Statistics: {len(all_memories)} total insights stored")
except Exception as e:
    print(f"Could not retrieve memory statistics: {e}")