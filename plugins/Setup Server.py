# from pyrogram import Client, filters
# import re
# from lib.utils import install_endpoint
# from db import savessh
# import requests
# import time
# 
# @Client.on_message(filters.command("setupserver"))
# def setup_server(c, m):
#   try:
#     if len(m.command) < 3:
#      raise Exception("Để thiết lập điểm cuối tự động, vui lòng cung thực hiện theo mẫu:\n\n1) thêm máy chủ SSH bằng lệnh /addserver\n2) chạy lệnh theo mẫu ```cmd\n/setupserver + tên máy + (cổng HTTP endpoint)\n```")
#      
#     user_id = m.from_user.id
#     machine = m.command[1]
#     http_port = m.command[2]
#     hostname, username, password, ssh_port = savessh.get(user_id, machine)
#     handle = install_endpoint(hostname, username, password, ssh_port, http_port)
#     st = m.reply(handle, quote=True)
#   except Exception as e:
#     st = m.reply(str(e), quote=True)
#   time.sleep(60)
#   st.delete()
#   m.delete()
#   