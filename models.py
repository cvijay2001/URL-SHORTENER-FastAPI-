from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class URLShortenerModel(Base):
    __tablename__ = "url_shortener"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    uni_code = Column(String, unique=True, index=True,default=None)
    og_url = Column(String)
    short_url = Column(String, index=True)
    alias = Column(String(10),index=True,default=None)

