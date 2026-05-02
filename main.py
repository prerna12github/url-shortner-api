import secrets
from datetime import datetime
from turtle import st
from fastapi import FastAPI, HTTPException
from fastapi.requests import HTTPConnection
from fastapi.responses import RedirectResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from api.database import get_code, get_record, set_record
import starlette.status as status

app = FastAPI()

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{short_code}")
def redirect_url(short_code: str):
    record = get_record(short_code)
    if record:
        return RedirectResponse(url=record, status_code=status.HTTP_302_FOUND)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/shorten")
def shorten_url(url: str):
    base = 'www.xyz.com'
    code = get_code(url)
    if code:
        return f"{base}/{code}"         
    short_code = secrets.token_urlsafe(6)
    set_record(url, short_code)
    return f"{base}/{short_code}"

    