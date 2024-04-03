
from fastapi import Depends, FastAPI, Response, status, HTTPException, Query
from sqlmodel import Session, Session, SQLModel, create_engine, select, column
from db.databaseConn import get_session, engine
from db import models
from typing import Optional
import router_file 
import router_model

app = FastAPI()

def create_db_and_tables():
    models.SQLModel.metadata.create_all(bind=engine)

app.include_router(router_file.router)
app.include_router(router_model.router)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.get(path="/")
async def read_root(*, session: Session = Depends(dependency=get_session)):
    return {"Hello": "This is LLM dcoument embeddings"}        







