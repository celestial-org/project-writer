from db.base import note_users as db


def save(user):
  name = user.first_name
  user_id = user.id
  username = user.username
  data = {"username": username, "user_id": user_id}
  db.put(data=data, key=name)