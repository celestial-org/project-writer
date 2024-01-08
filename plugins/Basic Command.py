from pyrogram import Client, filters
from lib.env import config_tool

@Client.on_message(filters.command("helps"))
def help_list(c, m):
  m.reply(f"""Xin chào **{m.from_user.first_name}**(`{m.from_user.id}`), dưới đây là danh sách lệnh khả dụng:
  
/get - Lấy liên kết tổng hợp subscribe

/add - Thêm subscribe 

/share - Chia sẻ subscribe 

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
  	
/addpoint + `prefix` + `endpoint url` - Bổ sung máy chủ test

/endpoints - Lấy danh sách lệnh test

/delpoint + `prefix` - Xoá máy chủ test chỉ định 

/install - Hướng dẫn cài điểm cuối

/setupserver - Cài đặt điểm cuối tự động (cần thêm máy chủ SSH)

/addserver - Thêm máy chủ SHH

/delserver - Xoá máy chủ SSH 

/machines - Danh sách máy chủ SSH đã thêm 

/cmd - Chạy lệnh shell trên máy chủ SSH
""", quote=True
)

@Client.on_message(filters.command("install"))
def help_install_endpoint(c, m):
  m.reply("**Docker:**```bash\ndocker run -d -p 80:8080 mymaking/test-endpoint:main\n```", quote=True)

@Client.on_message(filters.command(["start","help"]))
def send_welcome(c, m):
  m.reply_text(f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)\nDùng lệnh /helps để biết thêm chi tiết", quote=True)