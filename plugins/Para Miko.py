from pyrogram import Client, filters, enums
import re
import paramiko
import requests
import time 
from db import savessh

@Client.on_message(filters.command("addserver"))
def save_ssh_login(c, m):
  try:
    if m.chat.type != enums.ChatType.PRIVATE:
      raise Exception("Để bảo mật, vui lòng thực hiện thao tác này ở chat riêng tư")
    if len(m.command) < 5:
      raise Exception("Không đủ tham số")
    if len(m.command) == 5:
      _, machine, host, sshuser, passwd = m.command
      port = 22
    else:
      _, machine, host, sshuser, passwd, port = m.command
    user_id = m.from_user.id
    savessh.add(user_id, machine, host, sshuser, passwd, port)
    st = m.reply(f"Máy chủ với tên {machine} đã được lưu", quote=True)
    time.sleep(10)
  except Exception as e:
    st = m.reply(str(e), quote=True)
  time.sleep(20)
  st.delete()
  m.delete()
  
@Client.on_message(filters.command("delserver"))
def delete_machine_server(c, m):
  try:
    if len(m.command) < 2:
      raise Exception("Vui lòng cung cấp tên máy")
    machine = m.command[1]
    user_id = m.from_user.id
    try:
      savessh.delete(user_id, machine)
    except Exception as e:
      raise Exception(str(e))
    st = m.reply(f"Đã xoá máy chủ {machine}", quote=True)
  except Exception as e:
    st = m.reply(str(e), quote=True)
  time.sleep(20)
  st.delete()
  m.delete()
      
    