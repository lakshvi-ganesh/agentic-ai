import numpy as np
from sentence_transformers import SentenceTransformer
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from PyPDF2 import PdfReader
import os
 
data= r"C:\Users\labuser\Downloads\Leave-Policy.pdf"

reader=PdfReader(data)
 
raw_text="\n".join([i.extract_text() for i in reader.pages])
 
print(raw_text)
 
model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
 
def create_chunk (text,chunk_size=700,overlap=300):
    chunk=[]
    start=0
    while start < len(text):
        enf=start+ chunk_size
        chunk.append(text[start:enf])
        start+=chunk_size-overlap
    return chunk
 
chunk=create_chunk(raw_text)
print(len(chunk))
 
from qdrant_client import QdrantClient
 
# qdrant_client = QdrantClient(
#     url="https://2543a2f2-5f64-4138-8609-b837c507a92a.us-west-1-0.aws.cloud.qdrant.io:6333",
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzYzMDEwNzQ2fQ.Rk4wDaZX_nH5mT3ptURTKmCg9KKsoQxENx4LB8gLGI4",
# )
qdrant_client = QdrantClient(
    url="https://474a41b1-f0b5-4575-9dff-0c540a212eca.us-west-2-0.aws.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ccrS7tWpVqZjmJrPdbt5d2SHWPpG_-YJXaaDlbFvy6Q",
)
 
print(qdrant_client.get_collections())
 
embedding_data=model.encode(chunk).astype('float32')
 
 
collection_name="ins_data"
 
from qdrant_client.models import Distance, VectorParams, PointStruct
 
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384,distance=Distance.COSINE)
)
 
import uuid
 
point=[PointStruct(id = str(uuid.uuid4()), vector=embedding, payload={'chunk':chunk_})
       for chunk_, embedding in zip(chunk,embedding_data)]
 
qdrant_client.upsert(collection_name="ins_data",points=point)
