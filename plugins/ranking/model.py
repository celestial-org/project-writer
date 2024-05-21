import os
from sqlalchemy import create_engine, Column, BigInteger, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "rank"
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    exp = Column(BigInteger, default=0)


class DailyUser(Base):
    __tablename__ = "dailyrank"
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    exp = Column(BigInteger, default=0)
    level = Column(BigInteger, default=0)


class DB:
    def __init__(self):
        db_url = os.getenv("NEON_URL")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def update(
        self, user_id: int, first_name: str, last_name: str, username: str, exp: int
    ):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if user:
            exp = exp + user.exp
        user = User(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            exp=exp,
        )
        self.session.merge(user)
        self.session.commit()

    def get(self, user_id):
        return self.session.query(User).filter_by(user_id=user_id).first()

    def list(self):
        return self.session.query(User).all()

    def daily_add(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        username: str,
        exp: int,
        level: int,
    ):
        user = self.session.query(DailyUser).filter_by(user_id=user_id).first()
        if user:
            exp = exp + user.exp
        user = DailyUser(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            exp=exp,
            level=level,
        )
        self.session.merge(user)
        self.session.commit()

    def daily_get(self, user_id):
        return self.session.query(DailyUser).filter_by(user_id=user_id).first()

    def daily_list(self):
        return self.session.query(DailyUser).all()

    def reset_daily(self):
        users = self.session.query(DailyUser).all()
        for user in users:
            user.exp = 0
        self.session.commit()
