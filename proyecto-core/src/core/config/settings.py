import os
from dotenv import load_dotenv

load_dotenv()

# AI Provider Settings
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEFAULT_AI_PROVIDER = "deepseek"  # Forzar DeepSeek como predeterminado
