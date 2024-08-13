from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Manager, Preset, Note, Subscription
from environment import db_url


class Turso:
    def __init__(self) -> None:
        engine = create_engine(
            db_url, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()


class Database(Turso):
    def add_note(self, title: str, auth_id: int) -> None:
        if not self.session.query(Note).filter_by(title=title).first():
            note = Note(title=title, auth_id=auth_id)
            self.session.add(note)
            self.session.commit()

    def update_note(self, note: Note) -> None:
        self.session.merge(note)
        self.session.commit()

    def get_note(self, title: str) -> Note | None:
        return self.session.query(Note).filter_by(title=title).first()

    def remove_note(self, title: str) -> None:
        self.session.query(Note).filter_by(title=title).delete()
        self.session.commit()

    def list_notes(self) -> list:
        return self.session.query(Note).all()

    def add_subscription(self, note_title: str, url: str) -> bool:
        if self.session.query(Subscription).filter_by(note=note_title, url=url).first():
            return False
        subscription = Subscription(note=note_title, url=url)
        self.session.add(subscription)
        self.session.commit()
        return True

    def remove_subscription(self, note_title: str, url: str) -> bool:
        if (
            not self.session.query(Subscription)
            .filter_by(note=note_title, url=url)
            .first()
        ):
            return False
        self.session.query(Subscription).filter_by(note=note_title, url=url).delete()
        self.session.commit()
        return True

    def list_subscriptions(self, note_title: str) -> list:
        subs = self.session.query(Subscription).filter_by(note=note_title).all()
        if isinstance(subs, list):
            return [sub.url for sub in subs]
        return []

    def get_preset(self, name: str) -> Preset | None:
        return self.session.query(Preset).filter_by(name=name).first()

    def list_presets(self) -> list:
        return self.session.query(Preset).all()

    def add_preset(self, name: str, data: str) -> None:
        if not self.session.query(Preset).filter_by(name=name).first():
            preset = Preset(name=name, data=data)
            self.session.add(preset)
            self.session.commit()

    def remove_preset(self, name: str) -> None:
        self.session.query(Preset).filter_by(name=name).delete()
        self.session.commit()

    def list_managers(self) -> list:
        return self.session.query(Manager).all()

    def get_manager(self, name: str) -> Manager | None:
        return self.session.query(Manager).filter_by(name=name).first()

    def add_manager(self, name: str, api_key: str) -> None:
        if not self.session.query(Manager).filter_by(name=name).first():
            manager = Manager(name=name, api_key=api_key)
            self.session.add(manager)
            self.session.commit()

    def remove_manager(self, name: str) -> None:
        self.session.query(Manager).filter_by(name=name).delete()
        self.session.commit()
