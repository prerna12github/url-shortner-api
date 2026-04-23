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
async def get_code(code:str,db:Session=Depends(get_db)):
    db_url= db.query(URLModel).filter(URLModel.short_code==code).first()
    if db_url:
        db_url.click += 1
        db.commit()
        return RedirectResponse(url=db_url.original_url)
    else:
        raise HTTPException(status_code=404, detail="url not found")
    
@app.get("/shorten/stats/{code}")
async def get_stats(code:str,db:Session=Depends(get_db)):
    db_code=db.query(URLModel).filter(URLModel.short_code==code).first()
    if db_code:
        return {
            "short_code": code,
            "original_url": db_code.original_url,
            "clicks": db_code.click,
            "created_at": db_code.created_at
        }
    else:
        raise HTTPException(status_code=404, detail="url not found")

