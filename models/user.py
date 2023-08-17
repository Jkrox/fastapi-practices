from config.database import base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class User(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    