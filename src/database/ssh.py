from deta import Deta
from environment import deta_key


class SSH:

    def __init__(self, user_id: int):
        deta = Deta(deta_key)
        self.id = user_id
        self.db = deta.Base("ssh")

    def add(self, machine: str, host: str, user: str, passwd: str, port: int):
        existing_data = self.db.get(str(self.id))
        if existing_data:
            existing_list = existing_data.get("value", [])
            new_data = {
                "machine": machine,
                "host": host,
                "user": user,
                "passwd": passwd,
                "port": port,
            }
            existing_list.append(new_data)
            self.db.update({"value": existing_list}, key=str(self.id))
        else:
            data = [
                {
                    "machine": machine,
                    "host": host,
                    "user": user,
                    "passwd": passwd,
                    "port": port,
                }
            ]
            self.db.put(data=data, key=str(self.id))
        return "OK"

    def get(self, machine: str):
        user_data = self.db.get(str(self.id))
        if user_data:
            data_list = user_data.get("value", [])
            for entry in data_list:
                if entry["machine"] == str(machine):
                    match = entry
                    break
            try:
                return match["host"], match["user"], match["passwd"], match["port"]
            except Exception as e:
                raise Exception(f"Không tìm thấy thông tin máy chủ của bạn\n{e}")
        else:
            raise Exception("Bạn chưa lưu máy chủ nào!")

    def delete(self, machine: str):
        user_data = self.db.get(str(self.id))
        if user_data:
            data_list = user_data.get("value", [])
            updated_data_list = [
                entry for entry in data_list if entry["machine"] != machine
            ]
            self.db.update({"value": updated_data_list}, key=str(self.id))
            return "OK"
        else:
            raise Exception("Bạn chưa lưu máy chủ nào!")

    def machines(self):
        user_data = self.db.get(str(self.id))
        if user_data:
            data_list = user_data.get("value", [])
            machine_names = [entry.get("machine") for entry in data_list]
            return machine_names
        else:
            raise Exception("Bạn chưa lưu máy chủ nào!")
