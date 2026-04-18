from fastapi import FastAPI
from pydantic import BaseModel
import secrets
app = FastAPI()

urls={}

class URL(BaseModel):
    url:str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/url_shorten")
async def url_shorten(url:URL):
    short_url={}
    short_code= secrets.token_urlsafe(5)
    short_url[short_code] = "http://localhost:8000/"+short_code
    return short_url



    

