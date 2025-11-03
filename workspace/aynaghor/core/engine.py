
import os
from .config import settings

class Engine:
    def __init__(self):
        self.use_gemini = settings.get('USE_GEMINI', False)
        # placeholder clients – will be filled later
        self.gemini_client = None
        self.localai_client = None

    def route(self, prompt: str) -> str:
        if self.use_gemini:
            return self.gemini_client.generate(prompt)
        else:
            return self.localai_client.generate(prompt)
