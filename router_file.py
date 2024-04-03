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
from metadata import file_metadata, model_metadata
from router_model import read_model

router = APIRouter(
    prefix="/files",
    tags=['files']
)

@router.get(path="/", response_model=list[models.FileImported])
async def read_file(url_file_name: Optional[str] = "", url_file_hash: Optional[str] = "", url_offset: int = 0, url_limit: int = Query(default=10, le=100, ge=1)):
    with Session(engine) as session:
        # statement = select(models2.FileImported).filter(models2.FileImported.file_name.contains(file_name_with_extension)).order_by((models2.FileImported.created_at.desc())).limit(url_limit)
        #files_by_name = session.exec(statement)
        files_by_name = session.exec(select(models.FileImported)\
                                     .filter(column("file_name").contains(url_file_name))\
                                     .filter(column("file_hash").contains(url_file_hash))\
                                     .offset(url_offset).limit(url_limit)\
                                     .order_by((models.FileImported.created_at.desc()))).all()
        if not files_by_name:
            raise HTTPException(status_code=404, detail=f"File with name {url_file_name} not imported yet!")
        return files_by_name

@router.get(path="/{fileId}", response_model=models.FileImported)
async def read_file(fileId: int):
    with Session(engine) as session:
        file = session.get(entity=models.FileImported, ident=fileId)
        if not file:
            raise HTTPException(status_code=404, detail=f"File with name {fileId} not imported yet!")
        return file
    

@router.put("/ImportFile")
async def embedd_file(url_model_name: ModelName, url_file_path: str):
    file_metadata_in = file_metadata(file_path_in=url_file_path)
    model_metadata_in = read_model(url_model_name.value)

    print(f"#################################### LLM MODUEL DATA { model_metadata_in['model_name']}")

    docs = fitz.open(url_file_path)

    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            separators=["\n\n", "\n", "(?<=\. )"],      #, " ", ""
            tokenizer=AutoTokenizer.from_pretrained(pretrained_model_name_or_path=url_model_name.value),
            chunk_size=int( model_metadata_in['chunk_size'] ),
            chunk_overlap=int( model_metadata_in['chunk_size'] / 10)
        )
    model = SentenceTransformer(model_metadata_in['model_name'])    
    ## WRITTE TO File_Importe TABLE
    with get_session() as session:
        file_insert = models.FileImported(file_path = url_file_path, 
                                file_name = file_metadata_in['file_name'], 
                                file_type = file_metadata_in['file_type'], 
                                file_hash = file_metadata_in['file_hash'],
                                file_pages = file_metadata_in['file_pages'],
                                file_size = file_metadata_in['file_size'],
                                model_metadata_id = model_metadata_in['model_id'])
        session.add(file_insert)
        session.commit()
        session.refresh(file_insert)
        file_id = file_insert.id
        #print(f"file id: {file_id}")

    ## WRITE TO THE pgembedd0000 TABLE 
        for page in docs:
            texts = text_splitter.split_text(page.get_text().replace('\x00', ''))
            chunk_no = 0
            for chunkx in texts:
                chunk_no += 1
                embedding_chunk = model.encode(sentences=clean(chunkx, bullets=True, lowercase=True,  extra_whitespace=True, dashes=True, trailing_punctuation=True))
                if model_metadata_in['model_dim']==384: 
                    emb = models.Embedd384(file_id = file_id, page_number = page.number, chunk_number = chunk_no, text_data = chunkx, embedded_data = embedding_chunk)
                if model_metadata_in['model_dim']==512: 
                    emb = models.Embedded512(file_id = file_id, page_number = page.number, chunk_number = chunk_no, text_data = chunkx, embedded_data = embedding_chunk)
                if model_metadata_in['model_dim']==768: 
                    emb = models.Embedded768(file_id = file_id, page_number = page.number, chunk_number = chunk_no, text_data = chunkx, embedded_data = embedding_chunk)
                if model_metadata_in['model_dim']==1024: 
                    emb = models.Embedd1024(file_id = file_id, page_number = page.number, chunk_number = chunk_no, text_data = chunkx, embedded_data = embedding_chunk)
                if model_metadata_in['model_dim']==1536: 
                    emb = models.Embedded1536(file_id = file_id, page_number = page.number, chunk_number = chunk_no, text_data = chunkx, embedded_data = embedding_chunk)
                session.add(instance=emb)
            session.commit()
            session.flush()
                
        if not file_id:
            raise HTTPException(status_code=404, detail=f"File with name {url_file_path} not imported yet!")
        return f"file_id: {file_id} , ################ file_metadata: {file_metadata_in}"