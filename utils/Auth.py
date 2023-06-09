from datetime import datetime, timedelta
from os import environ

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError

load_dotenv()


def create_access_token(data: dict):
    to_encode = data.copy()

    expires_delta = timedelta(
        minutes=int(environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
    )
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow()

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        environ.get('SECRET_KEY'),
        algorithm=environ.get('ALGORITHM')
    )
    return encoded_jwt


def decode(token):
    try:
        payload = jwt.decode(
            token.replace('Bearer ', ''),
            environ.get('SECRET_KEY'),
            algorithms=[environ.get('ALGORITHM')]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized',
            headers={"WWW-Authenticate": "Bearer"}
        )
