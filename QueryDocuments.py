from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from db.databaseConn import get_session
from db import models
from sqlalchemy import select
from unstructured.cleaners.core import clean
#from pgvector.sqlalchemy import Vector

text = "Which function is equivalent to ediff1d?"
# print(text)

# EMBEDDING_MODEL_NAME = 'sentence-transformers/bert-base-nli-mean-tokens' #768
# EMBEDDING_MODEL_NAME = 'multi-qa-MiniLM-L6-cos-v1'. #386
# EMBEDDING_MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2' # 768
# EMBEDDING_MODEL_NAME = 'mixedbread-ai/mxbai-embed-large-v1'
# EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2' # 384
# EMBEDDING_MODEL_NAME = 'facebook/bart-large' #1024
# EMBEDDING_MODEL_NAME =  "intfloat/multilingual-e5-large"
EMBEDDING_MODEL_NAME = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"


rec_text_splitter = RecursiveCharacterTextSplitter(
  chunk_size = 256,
  chunk_overlap = 40,
  length_function = len,
)
chunks = rec_text_splitter.split_text(text=text)
di1 = "384"

model = SentenceTransformer(model_name_or_path=EMBEDDING_MODEL_NAME)

session = get_session()

for i, _ in enumerate(chunks):
    query_embedding = model.encode(sentences=clean(chunks[i], bullets=True, lowercase=True, extra_whitespace=True, dashes=True, trailing_punctuation=True))
    #print(query_embedding)
    rs = session.scalars(select(models.Embedd384).order_by(models.Embedd384.embedded_data.l2_distance(query_embedding)). limit(limit=3)).all()
    for row in rs:
        print(f"########################. Row no:  {row.id}, page number: {row.page_number}, chunk number: {row.chunk_number},  CREATED_AT: {row.created_at} ############################ \n TEXT: {row.text_data} \n")

session.expunge_all()
session.close()
session.flush()



