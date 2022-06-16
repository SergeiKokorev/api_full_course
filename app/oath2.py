from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY = "58888c76c5b8483c9d3e271e06bab6b9e3cfac5819425b682d1e1b119f67b46f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt
