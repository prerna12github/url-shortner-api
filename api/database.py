import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import psycopg
from psycopg import Error
from glide import GlideClientConfiguration, GlideClient, NodeAddress, ServerCredentials

async def get_glide_client():
    address = [NodeAddress(host=os.environ.get("REDIS_HOST","localhost"), port=int(os.environ.get("REDIS_PORT", 6379)))]

    config = GlideClientConfiguration(
        addresses=address,
        credentials=ServerCredentials(username=os.environ.get("REDIS_USER"), password=os.environ.get("REDIS_PASS")),
        request_timeout=500
    )

    client = await GlideClient.create(config)
    return client


def get_connection():
    load_dotenv()
    return psycopg.connect(f"{os.environ.get('DATABASE_URL')}")

conn = get_connection()
if conn is None:
    raise RuntimeError("Cannot proceed without a database connection")
cursor = conn.cursor()

def set_record(url: str, short_code: str):
    try:
        cursor.execute(
            "INSERT INTO urls (original_url, short_code, clicks, created_at) VALUES (%s, %s, %s, %s)",
            (url, short_code, 0, datetime.now(timezone.utc)),  # fix 1
        )
        conn.commit()
        return short_code
    except Error:
        conn.rollback()
        return get_code(url) or short_code

def get_record(short_code: str):
    try:
        cursor.execute(                                         # fix 2, 3, 4
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = %s RETURNING original_url",
            (short_code,),
        )
        row = cursor.fetchone()
        conn.commit()
        return row[0] if row else None
    except Error:
        conn.rollback()
        return None

async def get_code(url: str):
    try:
        client = await get_glide_client()
        code = await client.get(url)
        if code is not None:
            return code.decode("utf-8")
        cursor.execute("SELECT short_code FROM urls WHERE original_url = %s", (url,))
        row = cursor.fetchone()
        if row:
            await client.set(url, row[0])
        return row[0] if row else None
    except Error:
        return None
