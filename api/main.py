from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel, HttpUrl
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import secrets
from models import URL as URLModel
from database import Session as SessionLocal
from datetime import datetime
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class URL(BaseModel):
    url:HttpUrl

@app.get("/")
def read_root():
    return {"Hello": "Users"}

@app.post("/shorten")
async def url_shorten(url:URL,db:Session=Depends(get_db)):
    url_str = str(url.url) 
    existing = db.query(URLModel).filter(URLModel.original_url==url_str).first()
    if existing:
        return {"short_code": existing.short_code, "short_url": "https://url-shortner-api-one.vercel.app/"+existing.short_code}
    short_code = secrets.token_urlsafe(5)
    new_url = URLModel(short_code=short_code, original_url=url_str)
    db.add(new_url)
    db.commit()
    return {"short_code":short_code, "short_url": "https://url-shortner-api-one.vercel.app/"+short_code}
    
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
    
@app.get("/shorten/{code}")
async def get_code(code:str,db:Session=Depends(get_db)):
         db_url= db.query(URLModel).filter(URLModel.short_code==code).first()
         if db_url:
            now = datetime.utcnow()
            age = now-db_url.created_at
            days_old=age.days
            if days_old <= 30:
                db_url.click += 1
                db.commit()
                return RedirectResponse(url=db_url.original_url)
            else:
                raise HTTPException(status_code=404, detail="This link has expired")
         else:
          raise HTTPException(status_code=404, detail="url not found")
    


