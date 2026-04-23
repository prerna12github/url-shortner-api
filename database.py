from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from models import Base


engine = create_engine("sqlite:///./urldb.db",echo=True, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)
Session = sessionmaker(engine, autocommit=False, autoflush=False)

