import jwt
from datetime import datetime, timedelta



def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiration time, e.g., 15 minutes
        expire = datetime.utcnow() + timedelta(minutes=15) 
    
    # Add standard claims: expiration (exp) and issued at (iat)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    # Encode and sign the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == '__main__':
    # --- Example Usage ---

    # 1. Define the claims (payload data)
    user_data = {
        "sub": "123", # Subject (user ID)
        "name": "Md Rehan",
        "role": "Super User"
    }

    # 2. Create the token
    token = create_access_token(user_data)
    print(f"Generated JWT: {token}")

    # 3. (Optional) Verify and decode the token
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {decoded_payload}")
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
