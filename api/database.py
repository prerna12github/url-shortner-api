from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

Base.metadata.create_all(bind=engine)
Session = sessionmaker(engine, autocommit=False, autoflush=False)

