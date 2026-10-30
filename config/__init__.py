"""Runtime settings for Knowlix. Change these, not the code."""
import os

MAX_ITERATIONS = 6          # hard cap on reasoning steps (the judges check for a guard like this)
MAX_SAME_TOOL_CALLS = 2     # same tool + same args more than this => force a final answer

# Google Gemini Configuration (Sole AI Provider)
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
GEMINI_EMBEDDING_MODEL = os.environ.get("GEMINI_EMBEDDING_MODEL", "text-embedding-004")
TEMPERATURE = 0.2

# Database & Storage
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./knowlix.db")
DATA_DIR = os.environ.get("AGENTX_DATA_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))

# Security & Authentication
JWT_SECRET = os.environ.get("JWT_SECRET", "knowlix-super-secret-development-key-change-in-production")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

