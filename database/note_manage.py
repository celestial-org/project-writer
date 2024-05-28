import os
from deta import Deta
from hydrogram.types import User

deta_key = os.getenv("DETA_KEY")


class NoteManage:

    def __init__(self):
        deta = Deta(deta_key)
        self.base = deta.Base("managers")

    def add(self, user: User):
        self.base.put(
            data=str(user),
            key=str(user.id),
        )
        return user

    def remove(self, user: User):
        self.base.delete(str(user.id))

    def get(self, user):
        return self.base.get(str(user.id))
