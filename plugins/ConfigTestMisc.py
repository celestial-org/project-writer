from pyrogram import Client, filters
from db import save
from db import endpoints as ep


@Client.on_message(filters.command("endpoints"))
def list_endpoints(c, m):
  tests = ep.get_list()
  endpoints = "\n".join(tests)
  echo = f"```hướng dẫn:\nsử dụng lệnh /test với tiền tố của điểm cuối để sử dụng điểm cuối đó\n```\n**Danh sách: (tiền tố + nhà tài trợ)**\n"
  text = echo + endpoints
  m.reply(text, quote=True)
  
@Client.on_message(filters.command("addpoint"))
def add_endpoint(c, m):
  if len(m.command) < 3:
    m.reply("**Lỗi:**\nVui lòng làm theo mẫu để thêm điểm cuối\n```guide\n/addpoint + tiền tố + url điểm cuối\nví dụ: /addpoint vn http://103.0.0.0:80\n```", quote=True)
    return
  try:
    prefix = m.command[1]
    if prefix > 3:
      m.reply("Tiền tố tối đa là 3 ký tự. Vui lòng thừ lại", quote=True)
    endpoint = m.command[2]
    if not endpoint.startswith("http"):
      m.reply("Chỉ chấp nhận giao thức http/https", quote=True)
      return
    sponsor = m.from_user.first_name
    sponsor_id = m.from_user.id
    ep.add(sponsor, sponsor_id, prefix, endpoint)
    m.reply(f"**{sponsor}** đã đóng góp vào hệ thống một điểm cuối với tiền tố {prefix}. Lệnh /test{prefix} đã có sẵn", quote=True)
  except:
    m.reply("**Lỗi:**\nVui lòng làm theo mẫu để thêm điểm cuối\n```guide\n/addpoint + tiền tố + url điểm cuối\nví dụ: /addpoint vn http://103.0.0.0:80\n```", quote=True)
  
@Client.on_message(filters.command("killpoint"))
def remove_endpoint(c, m):
  if len(m.command) != 2:
    m.reply("Vui lòng cung cấp tiền tố điểm cuối cần xoá", quote=True)
    return
  prefix = m.command[1]
  uid = m.from_user.id
  try:
    _, sid, __ = ep.get(prefix)
    if uid not in [int(sid), 5665225938]:
      m.reply(f"**{m.from_user.first_name} ** điểm cuối này không thuộc sở hữu của bạn, không thể hoàn thành thao tác xoá", quote=True)
      return
    ep.rm(prefix)
    m.reply("Đã xoá điểm cuối", quote=True)