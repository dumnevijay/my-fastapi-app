from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlmodel import select, Relationship
from .. import models, schemes, oauth2
from ..database import get_session
from typing import Any
from sqlalchemy.orm import selectinload
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemes.PostOut])
async def get_posts(session: AsyncSession = Depends(get_session), get_current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # Correctly select the Post model class
    # statement = select(post)
    # statement = select(models.Post).options(selectinload(models.Post.owner)).filter(models.Post.title.contains(search)).offset(skip).limit(limit)
    
    # statement = select(models.Post, func.count(models.Vote.post_id).label("votes")).options(selectinload(models.Post.owner)).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit)
    statement = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .options(selectinload(models.Post.owner))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .offset(skip)
        .limit(limit)
    )
    # Execute the statement asynchronously
    result = await session.exec(statement)
    # Get all results (result.all() directly returns the list)
    posts = result.all()
    # Return the list directly as per response_model
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemes.PostResponse)
async def create_posts(post: schemes.PostCreate, session: AsyncSession = Depends(get_session), get_current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, is_published=post.published)
    new_post = models.Post(owner_id=get_current_user.id, **post.dict())
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post



# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)  - 1]
#     return post

@router.get("/{id}", response_model=schemes.PostOut)
async def get_post(id: int, session: AsyncSession = Depends(get_session), get_current_user: models.User = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    # post = await session.get(models.Post, id, options=[selectinload(models.Post.owner)] )
    statement = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .options(selectinload(models.Post.owner))
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
    )

    result = await session.exec(statement)
    post = result.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
 
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, session: AsyncSession = Depends(get_session), get_current_user: models.User = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # # delete post
    # # find index of post
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = await session.get(models.Post, id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    if (post.owner_id != get_current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    
    await session.delete(post)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# async def update_post(id: int, post: Post, session: AsyncSession = Depends(get_session)):

#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *  """, (post.title, post.content, post.published, str(id),))
#     # update_post = cursor.fetchone()
#     # conn.commit()
#     update_post = await session.get(models.Post, id)

#     if update_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'post with id: {id} does not exist')
    
#     update_post.__dict__.update(post.dict(exclude_unset=True))
#     await session.merge(update_post)
#     await session.commit()
#     await session.refresh(update_post)  # Refresh the update_post object

#     return {"data": update_post}

@router.put("/{id}", response_model=schemes.PostResponse)
async def update_post(id: int, post: schemes.PostCreate, session: AsyncSession = Depends(get_session), get_current_user: models.User = Depends(oauth2.get_current_user)):

    db_post = await session.get(models.Post, id)

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    
    if (db_post.owner_id != get_current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')

    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)
    
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)

    return db_post