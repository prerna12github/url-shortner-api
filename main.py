import secrets
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.requests import HTTPConnection
from fastapi.responses import RedirectResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from api.database import get_record, set_record

app = FastAPI()

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{short_code}")
def redirect_url(short_code: str):
    record = get_record(short_code)
    if record:
        return f'{record}'
    raise HTTPException(status_code=404, detail="Not Found")


@app.post("/shorten")
def shorten_url(url: str):
    short_code = secrets.token_urlsafe(6)
    set_record(url, short_code)
    base = 'www.xyz.com'
    return f"{base}/{short_code}"