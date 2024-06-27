from os import getenv
from dotenv import load_dotenv

# Third-party imports
from utils import utilities


load_dotenv()


# API - host
API_HOST: str       = getenv("STUN_API_HOST", "0.0.0.0")
# API - port
API_PORT: int       = int(getenv("STUN_API_PORT", 8000))

# Peer - username
PEER_USERNAME: str  = getenv("PEER_USERNAME", utilities.generate_random_string(8))
# Peer - host
PEER_HOST: str      = getenv("PEER_HOST", "0.0.0.0")
# Peer - port
PEER_PORT: str      = int(getenv("PEER_PORT", utilities.generate_random_port()))

