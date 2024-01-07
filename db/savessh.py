from db.base import savessh as db

def save(user_id, machine, host, user, passwd, port):
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
       raise Exception("Không tìm thấy thông tin máy chủ của bạn")
  else:
    raise Exception("Bạn chưa lưu máy chủ nào!")
    
def mymachine(user_id):
    user_data = db.get(str(user_id))
    if user_data:
        data_list = user_data.get("data", [])
        machine_names = [entry.get("machine") for entry in data_list]
        return machine_names
    else:
      raise Exception("Bạn chưa lưu máy chủ nào!")