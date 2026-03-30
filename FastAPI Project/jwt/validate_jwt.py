import jwt
import yaml

# Load config
with open("secret.yaml", "r") as f:
    config = yaml.safe_load(f)

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]


def validate_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "data": decoded}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Invalid token"}