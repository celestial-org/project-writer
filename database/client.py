import os
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from hydrogram.types import User
from .model import Base, Manager, Note


class Turso:
    def __init__(self) -> None:
        DB_URL = os.environ.get("DB_URL")
        engine = create_engine(DB_URL)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def add(self, name: str, url: str, user_id: int) -> bool:
        note = self.get(name, user_id)
        if note:
            urls = note.urls.splitlines()
        else:
            urls = []
        if url in urls:
            return False
        urls.append(url)
        urls = "\n".join(urls)
        note = Note(name=name, urls=urls, user_id=user_id)
        self.session.merge(note)
        self.session.commit()
        return True

    def get(self, name: str, user_id: int) -> Note | None:
        sql = select(Note).where(and_(Note.name == name, Note.user_id == user_id))
        return self.session.scalars(sql).first()

    def delete(self, name: str, url: str, user_id: int) -> bool:
        note = self.get(name, user_id)
        if note:
            urls = note.urls.splitlines()
            if url in urls:
                urls.remove(url)
                urls = "\n".join(urls)
                note = Note(
                    name=note.name, urls=urls, content=note.content, user_id=user_id
                )
                self.session.merge(note)
                self.session.commit()
                return True
            return False
        return False

    def list(self, name: str, user_id: int) -> list | None:
        note = self.get(name, user_id)
        if note:
            return note.urls.splitlines()
        return None

    def update(self, note: Note) -> None:
        self.session.merge(note)
        self.session.commit()

    def object(self, name: str, urls: str, content: str, user_id: int) -> Note:
        return Note(name=name, urls=urls, content=content, user_id=user_id)


class NoteManage:
    def __init__(self) -> None:
        DB_URL = os.environ.get("DB_URL")
        engine = create_engine(DB_URL)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def add(self, user: User):
        manager = Manager(user_id=user.id, data=str(User))
        self.session.merge(manager)
        self.session.commit()
        return user

    def get(self, user: User):
        sql = select(Manager).where(user_id=user.id)
        return self.session.scalars(sql).first()

    def remove(self, user: User):
        manager = self.get(user)
        self.session.remove(manager)
        self.session.commit()


class Machine:
    def __init__(self) -> None:
        TURSO_URL = os.environ.get("TURSO_URL")
        engine = create_engine(
            TURSO_URL, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        self.session = Session(engine)
