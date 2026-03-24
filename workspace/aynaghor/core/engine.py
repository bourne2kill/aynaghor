
import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import settings

logger = logging.getLogger(__name__)

class Engine:
    def __init__(self):
        self.use_gemini = os.getenv('USE_GEMINI', 'true').lower() == 'true'
        self.gemini_client = None
        self.localai_client = None

        # Initialize the appropriate client
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize AI clients based on configuration"""
        if self.use_gemini:
            try:
                from modules.gemini import GeminiClient
                api_key = os.getenv('GEMINI_API_KEY')
                model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

                if not api_key:
                    logger.warning("GEMINI_API_KEY not found in environment variables")
                    return

                self.gemini_client = GeminiClient(api_key, model_name)
                logger.info("Gemini client initialized successfully")

            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.gemini_client = None
        else:
            try:
                from modules.localai import LocalAIClient
                host = os.getenv('LLM_HOST', 'http://localhost:8080')
                model = os.getenv('LLM_MODEL', 'llama2-7b-chat')

                self.localai_client = LocalAIClient(host, model)
                logger.info("LocalAI client initialized successfully")

            except Exception as e:
                logger.error(f"Failed to initialize LocalAI client: {e}")
                self.localai_client = None

    def route(self, prompt: str) -> str:
        """Route prompt to appropriate AI provider"""
        if not prompt.strip():
            return "🌙 Please whisper your story request to AYNAGH0R..."

        # Check if clients are available
        if self.use_gemini and self.gemini_client:
            try:
                return self.gemini_client.generate(prompt)
            except Exception as e:
                logger.error(f"Gemini generation failed: {e}")
                return f"⚠️ The Gemini oracle is silent: {str(e)[:100]}..."

        elif not self.use_gemini and self.localai_client:
            try:
                return self.localai_client.generate(prompt)
            except Exception as e:
                logger.error(f"LocalAI generation failed: {e}")
                return f"⚠️ The local spirits are unresponsive: {str(e)[:100]}..."

        # Fallback response if no clients are available
        return self._get_fallback_response(prompt)

    def _get_fallback_response(self, prompt: str) -> str:
        """Provide fallback response when AI clients are unavailable"""
        return f"""🌙 **AYNAGH0R - Configuration Needed** 🌙

Your story request: "{prompt}"

*The storytelling spirits are not yet awakened. To enable AI-powered dark fantasy generation:*

**For Gemini API (Recommended):**
1. Get your API key from: https://makersuite.google.com/app/apikey
2. Create a `.env` file with: `GEMINI_API_KEY=your_key_here`
3. Set `USE_GEMINI=true` in your `.env` file

**For Local AI:**
1. Set up a local AI server (Ollama, LocalAI, etc.)
2. Set `USE_GEMINI=false` in your `.env` file
3. Configure `LLM_HOST` and `LLM_MODEL` in your `.env` file

*Once configured, AYNAGH0R will weave dark fantasy tales from your prompts.*

**Current Configuration:**
- USE_GEMINI: {self.use_gemini}
- Gemini Client: {'✓' if self.gemini_client else '✗'}
- LocalAI Client: {'✓' if self.localai_client else '✗'}"""

    def health_check(self) -> dict:
        """Check the health of AI clients"""
        status = {
            "engine_status": "healthy",
            "use_gemini": self.use_gemini,
            "clients": {
                "gemini": {
                    "initialized": self.gemini_client is not None,
                    "healthy": False
                },
                "localai": {
                    "initialized": self.localai_client is not None,
                    "healthy": False
                }
            }
        }

        # Test Gemini connection
        if self.gemini_client:
            try:
                status["clients"]["gemini"]["healthy"] = self.gemini_client.test_connection()
            except:
                status["clients"]["gemini"]["healthy"] = False

        # Test LocalAI connection
        if self.localai_client:
            try:
                status["clients"]["localai"]["healthy"] = self.localai_client.test_connection()
            except:
                status["clients"]["localai"]["healthy"] = False

        return status
