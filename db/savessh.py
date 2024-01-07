from db.base import savessh as db

def save(user_id, machine, host, user, passwd, port=22):
  data = {"user_id": user_id, "host": host, "user": user, "passwd": passwd, "port": port}
  db.put(data=data, key=str(machine))
  return "OK"
  
def fill(machine):
  data = db.get(machine)
  user_id = data["user_id"]
  host  = data["host"]
  user = data["user"]
  passwd = data["passwd"]
  port = data["port"]
  return user_id, host, user, passwd, port
  