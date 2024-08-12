import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pyrogram.types import User
from .model import Base, Manager, BotOptions, Note, Subscription

class Turso:
    def __init__(self) -> None:
        DB_URL = os.environ.get("DB_URL")
        engine = create_engine(
            DB_URL, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        self.session = Session(engine)


class Options(Turso):
    def get_option(self, name: str) -> str:
        option = self.session.query(BotOptions).filter_by(name=name).first()
        return option.value if option else None

    def set_option(self, name: str, value: str) -> bool:
        option = self.session.query(BotOptions).filter_by(name=name).first()
        if not option:
            self.session.add(BotOptions(name=name, value=value))
        else:
            option.value = value
        self.session.commit()
        return True

    def delete_option(self, name: str) -> bool:
        option = self.session.query(BotOptions).filter_by(name=name).first()
        if option:
            self.session.delete(option)
            self.session.commit()
            return True
        return False

    def list_options(self):
        options = {
            "update-interval": self.get_option("update-interval"),
            "proxy": self.get_option("proxy"),
        }
        return options


class NoteDB(Turso):
    def add_link(self, note_name: str, url: str, user_id: int) -> bool:
        note = self.get_note(note_name)
        if not note:
            note = Note(
                title=note_name,
                auth_id=user_id,
            )
            self.session.add(note)

        subscription = Subscription(note=note_name, url=url)
        self.session.merge(subscription)
        self.session.commit()
        return True

    def delete_link(self, note_name: str, url: str) -> bool:
        self.session.query(Subscription).filter_by(note=note_name, url=url).delete()
        self.session.commit()
        return True

    def get_note(self, note_name: str) -> Note | None:
        return self.session.query(Note).filter_by(title=note_name).first()

    def update_note(self, note: Note) -> None:
        existing_note = self.get_note(note.title)
        if existing_note:
            existing_note.content = note.content
            self.session.commit()

    def list_links(self, note_name: str) -> list | None:
        subscriptions = self.session.query(Subscription).filter_by(note=note_name).all()
        return (
            [subscription.url for subscription in subscriptions]
            if subscriptions
            else None
        )

    def note_object(self, note_name: str, content: str, user_id: int) -> Note:
        return Note(title=note_name, content=content, auth_id=user_id)

    def list_notes(self) -> list:
        return self.session.query(Note).all()


class ManagerDB(Turso):
    def add(self, user: User):
        manager = Manager(user_id=user.id, data=str(user))
        self.session.merge(manager)
        self.session.commit()
        return user

    def get(self, user: User):
        return self.session.query(Manager).filter_by(user_id=user.id).first()

    def remove(self, user: User):
        manager = self.get(user)
        if manager:
            self.session.delete(manager)
            self.session.commit()

    def list_managers(self):
        return self.session.query(Manager).all()
