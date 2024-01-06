from pyrogram import Client, filters
import re
import paramiko
import requests
import time

@Client.on_message(filters.command("setupserver"))
def setup_server(c, m):
  if len(m.command) < 5:
    m.reply('Để thiết lập điểm cuối tự động, vui lòng cung thực hiện theo mẫu:\n\n /setupserver h=\"hostname\" u=\"login user\" pw=\"login password\" ssh=\"cổng SSH\" http=\"cổng cài đặt endpoint, mặc định là 80\"', quote=True)
    return
  pattern = re.compile(r'(\w+)="([^"]*)"')
  matches = pattern.findall(m.text)
  params = dict(matches)
  hostname = params.get('h')
  if not hostname:
    m.reply("hostname là tham số bắt buộc! Vui lòng thực hiện lại", quote=True)
    return
  username = params.get('u')
  if not username:
    m.reply("username là tham số bắt buộc! Vui lòng thực hiện lại", quote=True)
    return
  password = params.get('pw')
  if not password:
    m.reply("mật khẩu là tham số bắt buộc! Vui lòng thực hiện lại", quote=True)
    return
  ssh_port = params.get('ssh')
  if not ssh_port:
    m.reply("cổng kết nối là bắt buộc! Vui lòng thực hiện lại", quote=True)
    return
  http_port = params.get('http', 80)
  handle = run_server(hostname, username, password, ssh_port, http_port)
  m.reply(handle, quote=True)
  
def run_server(hostname, username, password, ssh_port, http_port):
  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, ssh_port, username, password)
    docker_command = f'docker run -d -p {http_port}:8989 ghcr.io/mymaking/test-endpoint:main'
    stdin, stdout, stderr = ssh.exec_command(docker_command)
    print(stdout.read().decode('utf-8'))
    while not stdout.channel.exit_status_ready():
        time.sleep(1)
        ssh.close()
        return f"Docker command completed with exit status: {stdout.channel.recv_exit_status()}"
  except Exception as e:
      return f"Error: {e}"