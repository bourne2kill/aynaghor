
from dotenv import load_dotenv
import os
load_dotenv()

settings = {
    "USE_GEMINI": os.getenv("USE_GEMINI", "false").lower() == "true",
    "GEMINI_KEY": os.getenv("GEMINI_KEY", ""),
    "LLM_HOST": os.getenv("LLM_HOST", "http://host.docker.internal:8000"),
}
