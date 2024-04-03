
from enum import Enum

class ModelName(str, Enum):
    mxbai_large_v1: str = "mixedbread-ai/mxbai-embed-large-v1"
    all_miniLM_L6_v2: str = "sentence-transformers/all-MiniLM-L6-v2"
    multi_qa_miniLM_L6_cos_v1: str = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
    all_mpnet_base_v2: str = "sentence-transformers/all-mpnet-base-v2"
    facebook_bart_large: str = "facebook/bart-large"
    intfloat_multilingual_e5_large: str = "intfloat/multilingual-e5-large"

