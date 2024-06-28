from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from constant import ALGORITHM, JWT_SECRET_KEY
from pydantic import BaseModel

from jose import jwt, ExpiredSignatureError
from pydantic import ValidationError
from .utils import read_data

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


async def get_current_user(token: str = Depends(reuseable_oauth)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        now_datetime = datetime.now()
        if token_data.exp < now_datetime.timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError, ExpiredSignatureError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = read_data().get(token_data.sub, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
