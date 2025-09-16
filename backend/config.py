import os
from dotenv import load_dotenv

class Settings():
    LETTA_API_KEY: str = os.getenv("LETTA_API_KEY")
    LETTA_PROJECT: str = os.getenv("LETTA_PROJECT")
    AGENT_ID: str = os.getenv("AGENT_ID")
    AUTH_KEY: str = os.getenv("AUTH_KEY")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

settings = Settings()