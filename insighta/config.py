import json
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

CREDENTIALS_PATH = Path.home() / ".insighta" / "credentials.json"

BASE_URL = os.environ.get(
    "INSIGHTA_API_URL",
    "https://profile-intelligence-api.up.railway.app"
)

def save_credentials(data):
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDENTIALS_PATH, "w") as f:
        json.dump(data, f)


def load_credentials():
    if CREDENTIALS_PATH.exists():
        with open(CREDENTIALS_PATH) as f:
            return json.load(f)
        
    return None


def clear_credentials():
    if CREDENTIALS_PATH.exists():
        CREDENTIALS_PATH.unlink()