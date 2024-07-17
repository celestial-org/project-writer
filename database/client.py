import os
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from pyrogram.types import User
from .model import Base, Manager, Note, BotOptions


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
        """
        Get option by name.

        Args:
            name (str): name of option

        Returns:
            str: Value of option
        """
        sql = select(BotOptions).where(BotOptions.name == name)
        return self.session.scalars(sql).first().value

    def set_option(self, name: str, value: str) -> bool:
        """
        Set option by name.

        Args:
            name (str): name of option
            value (str): value of option

        Returns:
            bool: True if success, False if failed
        """
        sql = select(BotOptions).where(BotOptions.name == name)
        option = self.session.scalars(sql).first()
        if not option:
            option = BotOptions(name=name, value=value)
            self.session.add(option)
        else:
            option.value = value
        self.session.commit()
        return True

    def delete_option(self, name: str) -> bool:
        """
        Delete option by name.

        Args:
            name (str): name of option

        Returns:
            bool: True if success, False if failed
        """
        sql = select(BotOptions).where(BotOptions.name == name)
        option = self.session.scalars(sql).first()
        if not option:
            return False
        self.session.delete(option)
        self.session.commit()
        return True

    def list_options(self):
        """
        List options from database.

        Returns:
            dict: Dictionary of options
        """
        options = {
            "update-interval": self.get_option("update-interval"),
            "proxy": self.get_option("proxy"),
        }
        return options


class NoteDB(Turso):
    def add_link(self, note_name: str, url: str, user_id: int) -> bool:
        """
        Add url to note or create new note if not exist.

        Args:
            note_name (str): name of note
            url (str): url to add
            user_id (int): telegram user id

        Returns:
            bool: True if success, False if failed
        """
        note = self.get_note(note_name)
        if note:
            urls = note.urls.splitlines()
        else:
            urls = []
        if url in urls:
            return False
        urls.append(url)
        urls = "\n".join(urls)
        note = Note(name=note_name, urls=urls, user_id=user_id)
        self.session.merge(note)
        self.session.commit()
        return True

    def delete_link(
        self,
        note_name: str,
        url: str,
    ) -> bool:
        """
        Delete url from note.

        Args:
            note_name (str): name of note
            url (str): url to delete

        Returns:
            bool: True if success, False if failed
        """
        note = self.get_note(note_name)
        if note:
            urls = note.urls.splitlines()
            if url in urls:
                urls.remove(url)
                urls = "\n".join(urls)
                note = Note(
                    name=note.name,
                    urls=urls,
                    content=note.content,
                    user_id=note.user_id,
                )
                self.session.merge(note)
                self.session.commit()
                return True
            return False
        return False

    def get_note(
        self,
        note_name: str,
    ) -> Note | None:
        """
        Get note by name and user id.

        Args:
            note_name (str): name of note

        Returns:
            Note: Note object
        """
        sql = select(Note).where(Note.name == note_name)
        return self.session.scalars(sql).first()

    def update_note(self, note: Note) -> None:
        """
        Update note.

        Args:
            note (Note): Note object
        """
        note = self.get_note(note.name)
        self.session.merge(note)
        self.session.commit()

    def list_links(self, note_name: str) -> list | None:
        """
        List links in note.

        Args:
            note_name (str): name of note
            user_id (int): telegram user id

        Returns:
            list: List of urls
        """
        note = self.get_note(note_name)
        if note:
            return note.urls.splitlines()
        return None

    def note_object(
        self, note_name: str, urls: str, content: str, user_id: int
    ) -> Note:
        """
        Create Note object.

        Args:
            note_name (str): name of note
            urls (str): urls to add
            content (str): content of note
            user_id (int): telegram user id

        Returns:
            Note: Note object
        """
        return Note(name=note_name, urls=urls, content=content, user_id=user_id)

    def list_notes(self) -> list:
        """
        List notes by user id.

        Returns:
            list: List of notes
        """
        sql = select(Note)
        return self.session.scalars(sql).all()


class ManagerDB(Turso):
    def add(self, user: User):
        """
        Add manager to database.

        Args:
            user (User): User object

        Returns:
            User: User object
        """
        manager = Manager(user_id=user.id, data=str(User))
        self.session.merge(manager)
        self.session.commit()
        return user

    def get(self, user: User):
        """
        Get manager from database.

        Args:
            user (User): User object

        Returns:
            Manager: Manager object
        """
        sql = select(Manager).where(Manager.user_id == user.id)
        return self.session.scalars(sql).first()

    def remove(self, user: User):
        """
        Remove manager from database.

        Args:
            user (User): User object
        """
        manager = self.get(user)
        self.session.delete(manager)
        self.session.commit()

    def list_managers(self):
        """
        List managers from database.

        Returns:
            list: List of managers
        """
        sql = select(Manager)
        return self.session.scalars(sql)
