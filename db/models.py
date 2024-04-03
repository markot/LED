
from typing import  Optional, List
from sqlmodel import Field, SQLModel, DateTime
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String
from sqlalchemy.sql import func
from datetime import datetime


class ModelsData(SQLModel):
    id: int = Field(default=None, primary_key=True) 
    model_name: str = Field(nullable=False)
    model_dim: int = Field(nullable=False)
    chunk_size: int = Field(nullable=False)

class ModelsMetaData(ModelsData, table=True):
    __tablename__ = "model_metadata"
    model_data: str = Field(String(length=10240), nullable=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

 
class FileMetaData(SQLModel):
    id: int = Field(default=None, primary_key=True) #, autoincrement=True
    model_metadata_id: int | None = Field(default=None, nullable=False, foreign_key="model_metadata.id")
    file_path: str = Field(String(length=1024), nullable=False)
    file_name: str = Field(String(length=256),  nullable=False, index=True)
    file_type: str = Field(String(length=32), nullable=False)
    file_size: int = Field(nullable=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

class FileImported(FileMetaData, table=True):
    __tablename__ = "file_imported"
    file_hash: str = Field(String(length=32768), nullable=True)

class FileImportedreas(FileMetaData):
    id: int

class EmbeddedMeta(SQLModel):
    id: int = Field(default=None, primary_key=True) #, autoincrement=True
    file_id: int | None = Field(default=None, nullable=False, foreign_key="file_imported.id")
    page_number: int = Field(nullable=False)
    chunk_number: int = Field(nullable=False)
    text_data: str = Field(String(length=32768), nullable=True)
    

class Embedded1536(EmbeddedMeta, table=True):
    __tablename__ = "embedded1536"
    embedded_data: List[float] = Field(default=None, sa_column=Column(Vector(1536)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

class Embedd1024(EmbeddedMeta, table=True):
    __tablename__ = "embedded1024"
    embedded_data: List[float] = Field(default=None, sa_column=Column(Vector(1024)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

class Embedded768(EmbeddedMeta, table=True):
    __tablename__ = "embedded768"
    embedded_data: List[float] = Field(default=None, sa_column=Column(Vector(768)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

class Embedded512(EmbeddedMeta, table=True):
    __tablename__ = "embedded512"
    embedded_data: List[float] = Field(default=None, sa_column=Column(Vector(512)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

class Embedd384(EmbeddedMeta, table=True):
    __tablename__ = "embedded384"
    embedded_data: List[float] = Field(default=None, sa_column=Column(Vector(384)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

#class Embedd1536Create(Embedd1536):
#    pass
