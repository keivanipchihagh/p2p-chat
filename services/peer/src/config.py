from os import getenv
from dotenv import load_dotenv

load_dotenv()

# API - host
API_HOST: str       = getenv("STUN_API_HOST", "0.0.0.0")
# API - port
API_PORT: int       = int(getenv("STUN_API_PORT", 8000))
