from sqlalchemy import String, BigInteger, Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    title = Column(String, primary_key=True)
    auth_id = Column(BigInteger, default=0)
    content = Column(String, default="")
    urls = Column(String, default="")


class Manager(Base):
    __tablename__ = "managers"
    user_id = Column(BigInteger, primary_key=True)
    data = Column(String)


class Preset(Base):
    __tablename__ = "presets"
    name = Column(String, primary_key=True)
    value = Column(String)
