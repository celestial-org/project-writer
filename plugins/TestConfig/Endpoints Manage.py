from pyrogram import Client, filters
from db import save
from db import endpoints as ep
import os 
import time

@Client.on_message(filters.command("setlocal") & filters.user(5665225938))
def set_local_endpoint(c, m):
  save.save(m.from_user)
  try:
    if len(m.command) > 1:
      ep.get(m.command[1])
      os.environ["ENDPOINT"] = m.command[1]
      st = m.reply("Đã chuyển đổi điểm cuối mặc định")
    else:
      del os.environ["ENDPOINT"]
      st = m.reply("Đã khôi phục điểm cuối mặc định")
  except Exception as e:
    st = m.reply(f"Lỗi: {e}", quote=True)
  time.sleep(20)
  st.delete()

@Client.on_message(filters.command("endpoints"))
def list_endpoints(c, m):
  save.save(m.from_user)
  tests = ep.get_list()
  endpoints = "\n".join(tests)
  echo = f"```hướng dẫn: /test+prefix```\n**Danh sách:**\n\n"
  text = f"{echo}{endpoints}"
  st = m.reply(text, quote=True)
  time.sleep(60)
  st.delete()
  m.delete()
  
@Client.on_message(filters.command("addpoint"))
def add_endpoint(c, m):
  save.save(m.from_user)
  try:
    if len(m.command) < 3:
      raise Exception("Vui lòng làm theo mẫu để thêm điểm cuối\n```guide\n/addpoint + tiền tố + url điểm cuối\nví dụ: /addpoint vn http://103.0.0.0:80\n```")
    prefix = m.command[1]
    if len(prefix) > 5:
      raise Exception("Tiền tố tối đa là 5 ký tự. Vui lòng thừ lại")
    endpoint = m.command[2]
    if not endpoint.startswith("http"):
      raise Exception("Chỉ chấp nhận giao thức http/https")
      return
    sponsor = m.from_user.first_name
    sponsor_id = m.from_user.id
    ep.add(sponsor, sponsor_id, prefix, endpoint)
    st = m.reply(f"**{sponsor}** đã đóng góp vào hệ thống một điểm cuối với tiền tố {prefix}. Lệnh /test{prefix} đã có sẵn", quote=True)
  except Exception as e:
    st = m.reply(f"```Lỗi:\n{e}\n```", quote=True)
  time.sleep(20)
  st.delete
  m.delete()
  
@Client.on_message(filters.command("delpoint"))
def remove_endpoint(c, m):
  save.save(m.from_user)
  try:
    if len(m.command) < 2:
      raise Exception("Vui lòng cung cấp tiền tố điểm cuối cần xoá")
    prefix = m.command[1]
    uid = m.from_user.id
    _, sid, __ = ep.get(prefix)
    if uid not in [int(sid), 5665225938]:
      raise Exception("điểm cuối này không thuộc sở hữu của bạn, không thể hoàn thành thao tác xoá")
    ep.rm(prefix)
    st = m.reply("Đã xoá điểm cuối", quote=True)
  except:
    st = m.reply(f"Lỗi: {e}", quote=True)
  time.sleep(20)
  st.delete()
  m.delete()