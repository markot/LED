# pip install pydantic_settings pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

dotenv_path = Path('../.env')

class EnvSettings(BaseSettings):
    pg_user: str 
    pg_password: str 
    pg_host: str 
    pg_port: str 
    pg_db: str 
    pg_env: str  

    #model_config = SettingsConfigDict(env_file=dotenv_path, extra='ignore' )
    class Config:
        dotenv_path

env_settings = EnvSettings()

# print(settings.pg_user)

# # Alternatively, you can create it from environment variables.
# import os

# CONNECTION_STRING = PGVector.connection_string_from_db_params(
#     pg_user=os.environ.get("PGVECTOR_USER", "postgres"),
#     pg_password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
#     pg_host=os.environ.get("PGVECTOR_HOST", "localhost"),
#     pg_port=int(os.environ.get("PGVECTOR_PORT", "5432")),
#     pg_database=os.environ.get("PGVECTOR_DATABASE", "postgres"),


# )
