import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Type64(Base):
    __tablename__ = "type64"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(Integer, default=0)


class Type6(Base):
    __tablename__ = "type6"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(Integer, default=0)


class Type5(Base):
    __tablename__ = "type6"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    point = Column(Integer, default=0)


class Database:
    def __init__(self):
        db_url = os.getenv("NEON_URL")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def update(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        username: str,
        point: int,
        model: int,
    ):
        if model == 64:
            MODEL = Type64
        elif model == 6:
            MODEL = Type6
        else:
            MODEL = Type5

        user = MODEL(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            point=point,
        )
        self.session.merge(user)
        self.session.commit()

    def get(self, user_id: int, model: int) -> bool:
        if model == 64:
            MODEL = Type64
        elif model == 6:
            MODEL = Type6
        else:
            MODEL = Type5
        user = self.session.query(MODEL).filter_by(user_id=user_id).first()
        if user and user.point > 0:
            return user

    def list64(self):
        return self.session.query(Type64).all()

    def reset(self):
        type64 = self.session.query(Type64).all()

        type6 = self.session.query(Type6).all()

        type5 = self.session.query(Type5).all()

        for user in type64:
            user.point = 0

        for user in type6:
            user.point = 0

        for user in type5:
            user.point = 0

        self.session.commit()
