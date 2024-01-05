from db.base import note_users as db


def save(user):
  name = user.first_name
  user_id = user.id
  username = user.username
  data = {"username": username, "name": name}
  db.put(data=data, key=str(user_id))