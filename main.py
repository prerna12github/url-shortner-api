import secrets
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.middleware.cors import CORSMiddleware
from api.database import get_code, get_record, set_record
import starlette.status as status
from urllib.parse import urlparse

app = FastAPI()

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.add_middleware(CORSMiddleware, allow_origins=["*"])
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
    result = urlparse(url)
    if not result.scheme or not result.netloc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL")
    base = 'www.xyz.com'
    code = get_code(url)
    if code:
        return f"{base}/{code}"         
    short_code = secrets.token_urlsafe(5)
    set_record(url, short_code)
    return f"{base}/{short_code}"

    