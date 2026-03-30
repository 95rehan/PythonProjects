import jwt
import yaml
from datetime import datetime, timedelta

# Load config
with open("secret.yaml", "r") as f:
    config = yaml.safe_load(f)

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]


def create_access_token(user_id: str, name: str, role: str):
    payload = {
        "sub": user_id,
        "name": name,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token