from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemes, models, database, oauth2
from sqlmodel import select

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemes.Vote, session: AsyncSession = Depends(database.get_session), get_current_user: models.User = Depends(oauth2.get_current_user)):
    
    # Check if post exists
    post = await session.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

    found_vote = await session.get(models.Vote, (get_current_user.id, vote.post_id))
    
    if( vote.dir == 1 ):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {get_current_user.id} has already voted on post {vote.post_id}")
        # here we create a new vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=get_current_user.id)
        session.add(new_vote)
        await session.commit()
        await session.refresh(new_vote)
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        await session.delete(found_vote)
        await session.commit()
        return {"message": "Successfully deleted vote"}