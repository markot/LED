import os
import hashlib
import fitz
from sentence_transformers import SentenceTransformer

def file_metadata(file_path_in: str):
    docs = fitz.open(file_path_in)

    file_pages = len(docs) # Number of pages of the document
    file_name = os.path.basename(file_path_in) # File name with extension 
    file_type = os.path.splitext(file_path_in) # File extension
    file_size = os.path.getsize(file_path_in) # File extension

    with open(file_path_in, 'rb') as f:
        data = f.read()
        sha256_returned = hashlib.sha256(string=data).hexdigest()
     # Result
    result_file = {
        "file_pages": int(file_pages),
        "file_name": file_name,
        "file_type": file_type[1],
        "file_size": int(file_size / 1024), # vlaue in kB
        "file_hash": sha256_returned,
        }
    return result_file

def model_metadata(model_name_in: str):
    model_sentece_transfoirmer=SentenceTransformer(model_name_or_path=model_name_in)
    chunk_size = model_sentece_transfoirmer.max_seq_length
    model_dim = model_sentece_transfoirmer.get_sentence_embedding_dimension()
    model_data = str(model_sentece_transfoirmer) #"Model" #

    result_model = {
        "model": model_data,
        "model_name": model_name_in,
        "chunk_size": chunk_size,
        "model_dim": model_dim,
    }
    return result_model