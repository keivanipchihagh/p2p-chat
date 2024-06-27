from os import getenv
from dotenv import load_dotenv

load_dotenv()

# API - host
API_HOST: str       = getenv("STUN_API_HOST", "0.0.0.0")
# API - port
API_PORT: int       = int(getenv("STUN_API_PORT", 80))
# API - workers
API_WORKERS: int    = int(getenv("STUN_API_WORKERS", 1))
# API - logging
API_LOG_LEVEL: str  = getenv("STUN_API_LOG_LEVEL", 'DEBUG').lower()
# API - reload
API_RELOAD: bool    = getenv("STUN_API_RELOAD", 'True').lower() in ('true', '1', 't')

# Redis - host
REDIS_HOST: str     = getenv("REDIS_HOST", "0.0.0.0")
# Redis - port
REDIS_PORT: int     = int(getenv("REDIS_PORT", 6379))
# Redis - password
REDIS_PASSWORD: str = getenv("REDIS_PASSWORD", "")
# Redis - db
REDIS_DB: int       = int(getenv("REDIS_DB", 0))
