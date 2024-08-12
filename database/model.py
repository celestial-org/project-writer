from sqlalchemy import String, BigInteger, Column, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    title = Column(String, primary_key=True)
    auth_id = Column(BigInteger, default=0)
    content = Column(String, default="")


class Subscription(Base):
    __tablename__ = "notes_subscriptions"

    note = Column(String)
    url = Column(String)

    __table_args__ = (PrimaryKeyConstraint("note", "url"),)


class Manager(Base):
    __tablename__ = "managers"
    user_id = Column(BigInteger, primary_key=True)
    data = Column(String)


class BotOptions(Base):
    __tablename__ = "bot_options"
    name = Column(String, primary_key=True)
    value = Column(String)
