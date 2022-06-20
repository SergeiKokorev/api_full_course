from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from . import schemas

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "58888c76c5b8483c9d3e271e06bab6b9e3cfac5819425b682d1e1b119f67b46f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])

    return encode_jwt


def verify_access_token(token: str, credential_exeption):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        id = payload.get("user_id")
    
        if not id:
            raise credential_exeption
    
        token_data = schemas.TokenData(id=id)
    except JWTError as er:
        raise credential_exeption


def get_current_user(token: str = Depends(oath2_scheme)):

    credential_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORAZED,
        detail='Could not validate credentials',
        header={'WWW-Authenticate': 'Bearer'}
    )

    return verify_access_token(token, credential_exeption)        
