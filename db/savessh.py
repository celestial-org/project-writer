from db.base import savessh as db

def add(user_id, machine, host, user, passwd, port):
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

  
def get(user_id, machine):
  user_data = db.get(str(user_id))
  if user_data:
    data_list = user_data.get("data", [])
    for entry in data_list:
       if entry.get("machine") == machine:
           return entry["host"], entry["user"], entry["passwd"], entry["port"]
       raise Exception("Không tìm thấy thông tin máy chủ của bạn")
  else:
    raise Exception("Bạn chưa lưu máy chủ nào!")
    
def delete(user_id, machine):
    user_data = db.get(str(user_id))
    if user_data:
        data_list = user_data.get("data", [])
        updated_data_list = [entry for entry in data_list if entry.get("machine") != machine]
        db.update({"data": updated_data_list}, key=str(user_id))
        return "OK"
    else:
      raise Exception("Bạn chưa lưu máy chủ nào!")
    
def machines(user_id):
    user_data = db.get(str(user_id))
    if user_data:
        data_list = user_data.get("data", [])
        machine_names = [entry.get("machine") for entry in data_list]
        return machine_names
    else:
      raise Exception("Bạn chưa lưu máy chủ nào!")