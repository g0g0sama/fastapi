from .database import Base
from sqlalchemy.sql.expression import null, text
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable= False)
    price = Column(Integer, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text("now()"))
    published = Column(Boolean, server_default= "True", nullable=False)