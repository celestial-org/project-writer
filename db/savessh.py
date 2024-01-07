from db.base import savessh as db

def save(user_id, machine, host, user, passwd, port=22):
    existing_data = db.get(str(user_id))
    if existing_data:
        existing_list = existing_data.get("data", [])
        new_data = {"machine": machine, "host": host, "user": user, "passwd": passwd, "port": port}
        existing_list.append(new_data)
        db.update({"data": existing_list}, key=str(user_id))
    else:
        data = [{"machine": machine, "host": host, "user": user, "passwd": passwd, "port": port}]
        db.put(data=data, key=str(user_id))
    return "OK"

  
def fill(user_id, machine):
  user_data = db.get(str(user_id))
  if user_data:
    data_list = user_data.get("data", [])
    for e in data_list:
       if e.get("machine") == machine:
           return e["host"], e["user"], e["passwd"], e["port"]
  