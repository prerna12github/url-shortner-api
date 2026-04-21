from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String
from datetime import datetime

class Base(DeclarativeBase):
    pass
class URL(Base):
    __tablename__ = "Url_Shorten"

    id : Mapped[int]=mapped_column(Integer,primary_key=True)
    short_code : Mapped[str]=mapped_column(String,unique=True)
    original_url : Mapped[str]=mapped_column(String)
    created_at : Mapped[datetime]=mapped_column(datetime, deafult=datetime.utcnow)
    
