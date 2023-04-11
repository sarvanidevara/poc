from fastapi import FastAPI
from app.features.user import router as UserRouter
from app.features.auth import router as AuthRouter
from app.features.post import router as PostRouter
from app.features.vote import router as VoteRouter
from .models import base
from .db.database import engine

base.Base.metadata.create_all(bind=engine)

app = FastAPI()  

app.include_router(UserRouter.router)
app.include_router(AuthRouter.router)
app.include_router(PostRouter.router)
app.include_router(VoteRouter.router)

@app.get("/")
def root():
    return {"message": "change API Works"}  