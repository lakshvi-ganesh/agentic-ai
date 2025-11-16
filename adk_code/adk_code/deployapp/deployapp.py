import os
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

agent_dir=os.path.dirname(os.path.abspath(__file__))

ALLOWED_URL=['*',"http://localhost:8085"]

SERVER_web=True

app : FastAPI=get_fast_api_app(
    agents_dir=agent_dir,
    allow_origins=ALLOWED_URL,
    web=SERVER_web
)


if __name__=='__main__':
    uvicorn.run(app,host="0.0.0.0",port=8085)