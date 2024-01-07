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
      st = m.reply("Đã chuyển đổi máy chủ test mặc định")
    else:
      os.environ["ENDPOINT"] = "vncmc"
      st = m.reply("Đã khôi phục máy chủ test")
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
      raise Exception("Vui lòng làm theo mẫu để thêm máy chủ test\n```guide\n/addpoint + tiền tố + url\nví dụ: /addpoint vn http://103.0.0.0:80\n```")
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
    st = m.reply(f"**{sponsor}** đã đóng góp máy chủ test mới với tiền tố {prefix}. Lệnh /test{prefix} đã có thể sử dụng", quote=True)
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
      raise Exception("Vui lòng cung cấp prefix máy chủ test cần xoá")
    prefix = m.command[1]
    uid = m.from_user.id
    _, sid, __ = ep.get(prefix)
    if uid not in [int(sid), 5665225938]:
      raise Exception("Máy chủ test này không thuộc sở hữu của bạn, không thể hoàn thành thao tác xoá")
    ep.rm(prefix)
    st = m.reply(f"Đã xoá máy chủ test **{prefix.upper()}**", quote=True)
  except:
    st = m.reply(f"Lỗi: {e}", quote=True)
  time.sleep(20)
  st.delete()
  m.delete()