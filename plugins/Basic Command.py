from pyrogram import Client, filters
from lib.env import config_tool

@Client.on_message(filters.command("helps"))
def help_list(c, m):
  m.reply(f"""Xin chào **{m.from_user.first_name}**(`{m.from_user.id}`), dưới đây là danh sách lệnh khả dụng:
  
/get - Lấy liên kết tổng hợp subscribe

/add - Thêm subscribe 

/share - Chia sẻ subscribe 

/test - Kiểm tra cấu hình v2ray

/mylist - Danh sách subscribe của tôi

/remove - Xoá subscribe khỏi danh sách

/checkall - Tự kiểm tra và xoá subscribe bị lỗi (không bao gồm subscribe hết lưu lượng truy cập)

/request [get, post, put, delete, option] - Gửi yêu cầu HTTP

/sharelist - Lấy danh sách note chung

/rmshare - Xoá subscribe khỏi note chung 

/checkshare - Kiểm tra và xoá khỏi note chung

/ext - Nâng cao
""", quote=True)

@Client.on_message(filters.command("ext"))
def ext_command_list(c, m):
  m.reply(f"""**{m.from_user.first_name}**(`{m.from_user.id}`), lệnh nâng cao:

/multitest - Kiểm tra cấu trúc v2ray đa máy chủ
  	
/addpoint - `None`

/testservers - Lấy danh sách máy chủ test

/delpoint - None

/install - Hướng dẫn cài đặt máy chủ test

/addserver - Thêm máy chủ SHH

/delserver - Xoá máy chủ SSH 

/machines - Danh sách máy chủ SSH đã thêm 

/cmd - Chạy lệnh shell trên máy chủ SSH
""", quote=True
)

@Client.on_message(filters.command("install"))
def help_install_endpoint(c, m):
  m.reply("**Docker:**```bash\ndocker run -d ghcr.io/bosuutap/writer-endpoint-installer:main\n```\n\nThiết lập thủ công:\n\n`git clone https://github.com/bosuutap/writer-endpoint-installer\npip install -r requirements.txt\nbash setup.sh\npython main.py", quote=True)

@Client.on_message(filters.command(["start","help"]))
def send_welcome(c, m):
  m.reply_text(f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)\nDùng lệnh /helps để biết thêm chi tiết", quote=True)