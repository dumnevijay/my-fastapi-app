from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import select
from .. import models, schemes, utils, oauth2
from ..database import get_session


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
async def create_user(user_credentials: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    # user = await session.get(models.User.email, user_credentials.email)
    statement = select(models.User).where(models.User.email == user_credentials.username).limit(1)
    result = await session.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}