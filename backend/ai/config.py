import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ==========================
# LLM Configuration
# ==========================

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.3-70b-versatile"
)

# ==========================
# API Keys
# ==========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================
# Validation
# ==========================

if LLM_PROVIDER.lower() == "groq" and not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )