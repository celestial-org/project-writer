import os
from sqlalchemy import create_engine, select, String, BigInteger
from sqlalchemy.orm import Session, Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    name: Mapped[str] = mapped_column(String, primary_key=True)
    urls: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(BigInteger)

    def __repr__(self) -> str:
        obj = dict(
            name=self.name,
            urls=self.urls.splitlines(),
            content=self.content,
            user_id=self.user_id,
        )
        return str(obj)


class Turso:
    def __init__(self) -> None:
        TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")
        dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"
        engine = create_engine(
            dbUrl, connect_args={"check_same_thread": False}, echo=True
        )
        self.session = Session(engine)

    def add(self, name: str, user_id: int, url: str) -> bool:
        sql = select(Note).where(Note.name == name)
        note = self.session.scalars(sql).first()
        urls = note.urls.splitlines()
        if url in urls:
            return False
        urls.append(url)
        urls = "\n".join(urls)
        note = Note(name=name, urls=urls, user_id=user_id)
        return True

    def delete(self, name: str, user_id: int) -> bool:
        return True

    def list(self, name: str, user_id: int) -> list:
        return []
