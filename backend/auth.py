from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import PyJWTError
from pydantic import BaseModel
import os
from typing import Optional

# Secret key setup
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "super_secret_for_dev")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class TokenData(BaseModel):
    user_id: Optional[str] = None

async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Token decode karna (PyJWT style)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # User ID nikalna (Assuming Better Auth puts id in 'sub' or 'id')
        user_id: str = payload.get("sub") or payload.get("id")
        
        if user_id is None:
            raise credentials_exception
        return user_id
    except PyJWTError:
        raise credentials_exception