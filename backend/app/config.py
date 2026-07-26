from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_API = "https://api.github.com"

settings = Settings()