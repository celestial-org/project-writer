from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Manager, Preset, Note
from environment import db_url


class Turso:
    def __init__(self) -> None:
        engine = create_engine(
            db_url, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()


class Database(Turso):
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

    def add_url(self, note_title: str, url: str) -> bool:
        note = self.get_note(note_title)
        if note:
            urls = note.urls.split("\n")
            if url not in urls:
                urls.append(url)
                note.urls = "\n".join(urls)
                self.session.merge(note)
                self.session.commit()
                return True
            return False
        return False
        

    def remove_url(self, note_title: str, url: str) -> bool:
        note = self.get_note(note_title)
        if note:
            urls = note.urls.split("\n")
            if url in urls:
                urls.remove(url)
                note.urls = "\n".join(urls)
                self.session.merge(note)
                self.session.commit()
                return True
            return False
        return False

    def list_urls(self, note_title: str) -> list:
        note = self.get_note(note_title)
        if note:
            return note.urls.split("\n")
        return []

    def get_preset(self, name: str) -> Preset | None:
        return self.session.query(Preset).filter_by(name=name).first()

    def list_presets(self) -> list:
        return self.session.query(Preset).all()

    def add_preset(self, name: str, data: str) -> None:
        if not self.session.query(Preset).filter_by(name=name).first():
            preset = Preset(name=name, value=data)
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
