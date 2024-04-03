from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Query, APIRouter
from sqlmodel import Session, Session, select, column
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer 
from unstructured.cleaners.core import clean

from db.databaseConn import get_session, engine
from db import models
from enumclass import ModelName
import fitz # install using: pip install PyMuPDF
from metadata import model_metadata



router = APIRouter(
    prefix="/models",
    tags=['models']
)

async def insert_new_model(new_model_name: str):
     with Session(engine) as session:
        model_metadata_in = model_metadata(model_name_in=new_model_name)
        model_insert = models.ModelsMetaData(
                                model_name = new_model_name,  
                                model_dim = model_metadata_in['model_dim'], 
                                chunk_size = model_metadata_in['chunk_size'],
                                model_data =  model_metadata_in['model'], )
        session.add(model_insert)
        session.commit()
        session.flush()

def read_model(url_model_name_read: str):
     with Session(engine) as session:
        model_exists = session.exec(select(models.ModelsMetaData).filter(column("model_name").contains(url_model_name_read))).first()
        if not model_exists:
            insert_model = insert_new_model(url_model_name_read)
            model_exists = session.exec(select(models.ModelsMetaData).filter(column("model_name").contains(url_model_name_read))).first()
        model_metada_return = {
               "model_id": model_exists.id,
               "model_dim": model_exists.model_dim,
               "chunk_size": model_exists.chunk_size,
               "model_name": url_model_name_read}
        return model_metada_return      

@router.get(path="/", response_model=list[models.ModelsData])
async def read_model_metadata(url_model_name: ModelName):
     with Session(engine) as session:
        model_exists = session.exec(select(models.ModelsMetaData).filter(column("model_name").contains(url_model_name.value))).all()
        if not model_exists:
            insert_model = insert_new_model(url_model_name.value)
            model_exists = session.exec(select(models.ModelsMetaData).filter(column("model_name").contains(url_model_name.value))).all()
            return model_exists
        return model_exists

