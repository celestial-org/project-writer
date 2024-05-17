import os
from sqlalchemy import create_engine, Column, BigInteger, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "rank"
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(500))
    last_name = Column(String(500), nullable=True)
    username = Column(String(500), nullable=True)
    exp = Column(BigInteger, default=0)


class DB:
    def __init__(self):
        db_url = os.getenv("MYSQL_URL")
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


def get_level(exp):
    level = 0
    require_exp = 100
    while exp >= require_exp:
        exp -= require_exp
        level += 1
        if level % 2 == 0:
            require_exp *= 1.2

    remaining_exp_for_next_level = require_exp - exp
    return level, round(remaining_exp_for_next_level)


def ranks_prettier(user_rows):
    ranks = []
    emojis = ["🏆", "🏅", "🥇", "🥈", "🥉"]
    sorted_users = sorted(user_rows, key=lambda x: x[1], reverse=True)
    for i, row in enumerate(sorted_users[:20]):
        rank = f"{emojis[i]}" if i < len(emojis) else f"{i + 1}"
        user_info = [
            f"<b>{rank}) {row[0]}</b>",
            f"(Lv{get_level(row[1])[0]})",
        ]
        ranks.append("  ".join(user_info))

    return ranks


def count_exp(m, level: int):
    exp = 1
    if m.text:
        exp = len(m.text)
        if exp == 4096:
            exp -= 4000
        elif exp > 4000:
            exp -= 3000
        if m.text.startswith("/share"):
            if any(scheme in m.text for scheme in ["http://", "https://"]):
                exp += exp * 2 + level
    elif m.video or m.audio or m.document:
        exp += 500 + level
    elif m.photo:
        exp += 300 + level
    elif m.sticker:
        exp += 50 + level
    if m.caption:
        exp += len(m.caption)
    if m.from_user.id == 6580709427:
        exp += 100
    return exp


def get_user_rank(user_rows, target_user_id):
    sorted_users = sorted(user_rows, key=lambda x: x[1], reverse=True)
    for i, (user_id, _) in enumerate(sorted_users, start=1):
        if user_id == target_user_id:
            return i
    return None


def get_title(level):
    if level < 20:
        return "Gà Mờ"
    elif level < 40:
        return "Nghiệp Dư"
    elif level < 60:
        return "Thông Thạo"
    elif level < 80:
        return "Lưu Loát"
    elif level < 101:
        return "Chuyên Nghiệp"
    elif level < 201:
        return "Bậc Thầy"
    elif level < 301:
        return "Vô Địch"
    elif level < 401:
        return "Bất Tử"
    elif level < 501:
        return "Chiến Thần"
    else:
        return "Vĩnh Hằng"
