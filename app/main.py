from fastapi import FastAPI
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API!"}


# As I am using alembic for migrations, there is no need for the init_db function to create the database when ever we create or run the app
# @app.on_event("startup")
# async def on_startup():
#     await init_db()


