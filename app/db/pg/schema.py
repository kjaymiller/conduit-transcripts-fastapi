import os

from dotenv import load_dotenv
from typing import Optional

from sqlmodel import (
    Field,
    SQLModel,
    create_engine,
)

from datetime import date

load_dotenv()

class Episode(SQLModel, table=True):
    __tablename__ = 'conduit_transcripts'
    __table_args__ = {'extend_existing':True}
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    date: date
    description: str
    url: str

engine = create_engine(os.getenv("POSTGRES_SERVICE_URI"))