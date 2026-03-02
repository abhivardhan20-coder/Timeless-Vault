import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite if PostgreSQL is not reachable
_pg_url = os.getenv("DATABASE_URL", "")
_use_sqlite = os.getenv("USE_SQLITE", "true").lower() == "true"

if _use_sqlite or not _pg_url:
    DATABASE_URL = "sqlite:///./vaultchain.db"
else:
    DATABASE_URL = _pg_url

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))