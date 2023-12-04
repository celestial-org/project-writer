from pyrogram import Client, filters
import platform, psutil, requests


def server_info():
  try:
    # Sử dụng ipinfo.io để lấy thông tin về địa chỉ IP
    response = requests.get('https://ipinfo.io')
    data = response.json()

    # Trích xuất thông tin từ dữ liệu JSON
    ip = data.get('ip', 'N/A')
    city = data.get('city', 'N/A')
    region = data.get('region', 'N/A')
    country = data.get('country', 'N/A')
    provider = data.get('org', 'N/A')

    server_info = f"IP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}\nProvider: {provider}"

  except Exception as e:
    server_info = f"Error: {e}"

  return server_info


@Client.on_message(filters.command('info'))
def bot_server_info(c, m):
  arch = platform.machine()
  ver = platform.version()
  name = platform.uname()
  system = platform.system()
  cpu_usage = psutil.cpu_percent()
  ram_info = psutil.virtual_memory()
  serverinfo = server_info()

  reply_text = (f'**SERVER:** \n`{serverinfo}`\n\n'
                f'**RAM:** \n`{ram_info}`\n\n**CPU:** \n`{cpu_usage}`\n\n'
                f'**INFO:** \n`{name}`\n\n**ARCHITECTURE:** \n`{arch}`\n\n'
                f'**VERSION:** \n`{ver}`\n**OS:** `{system}`')

  m.reply(reply_text)
