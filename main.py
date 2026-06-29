from typing import Annotated

from fastapi import FastAPI,Depends
from sqlalchemy.ext.asyncio import AsyncSession


from database import get_session



app = FastAPI()

db_session = Annotated[AsyncSession,Depends(get_session)]

@app.get("/")
async def root():
    return {"message": "Hello World"}
