from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import secrets
from models import URL as URLModel
from database import Session as SessionLocal
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class URL(BaseModel):
    url:str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/shorten")
async def url_shorten(url:URL,db:Session=Depends(get_db)):
    short_code= secrets.token_urlsafe(5)
    new_url = URLModel(short_code=short_code, original_url=url.url)
    db.add(new_url)
    db.commit()
    return {"short_code":short_code, "short_url": "http://localhost:8000/"+short_code}

@app.get("/shorten/{code}")
async def get_code(code:str):
    if code in urls:
        code_url= urls.get(code)
        return RedirectResponse(url=code_url)
    else:
        raise HTTPException(status_code=404, detail="url not found")
    

