from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
 
 
 
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
 
from sentence_transformers import SentenceTransformer
model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
 
 
collection="ins_data"
 
def qdrant_data(query:str):
    print(query)
    en_query=model.encode(query).tolist()
    result=qdrant_client.search(
        collection_name=collection,
        query_vector=en_query,
        limit=3
    )
    return "\n".join([ d.payload["chunk"] for d in result])
 
retriever_tool=FunctionTool(qdrant_data)
 
root_agent=LlmAgent(
    name="myapp",
    model='gemini-2.0-flash',
    instruction="""
    you are an helpful assistant who uses below context and generate or respond to user query in short , clear and complete based on question
    if you don't find the info say I coundn't find it in the document don't create answer and alway call tool to answer user query
 
    """,
    description="chat application based on google adk freamework and gemini as llm ",
    tools=[retriever_tool]
 
)
 
