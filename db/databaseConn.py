# 
#import os
from sqlmodel import create_engine, SQLModel, Session

from urllib import parse 
from db.config import env_settings
from functools import lru_cache
from contextlib import contextmanager


@lru_cache
def get_settings():
    return env_settings

#print (get_settings().pg_user)

engine = create_engine(url=f"postgresql://{get_settings().pg_user}:{parse.quote(get_settings().pg_password)}@{get_settings().pg_host}:{get_settings().pg_port}/{get_settings().pg_db}") #, echo=True)

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    SQLModel.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()




# Base = declarative_base()


