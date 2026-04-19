from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import secrets
app = FastAPI()

urls={}

class URL(BaseModel):
    url:str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/url_check")
async def url_shorten(url:URL):
    short_code= secrets.token_urlsafe(5)
    urls[short_code] = url.url
    return {"short_code":short_code, "short_url": "http://localhost:8000/"+short_code}

@app.get("/url_check/{code}")
async def get_code( code):
    if code in urls:
        code_url= urls.get(code)
        return RedirectResponse(url=code_url)
    else:
        raise HTTPException(status_code=404, detail="url not found")
    

