from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,DateTime
from datetime import datetime
from database import Base

class URL(Base):
    __tablename__ = "Url_Shorten"

    id : Mapped[int]=mapped_column(Integer,primary_key=True)
    short_code : Mapped[str]=mapped_column(String,unique=True)
    original_url : Mapped[str]=mapped_column(String)
    created_at : Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    
