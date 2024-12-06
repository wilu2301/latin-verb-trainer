from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, CHAR


class Base(DeclarativeBase):
    pass


class Verb(Base):
    __tablename__ = "Verbs"

    id = Column(Integer, primary_key=True)
    declination = Column(CHAR)



