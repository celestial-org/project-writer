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
/sharelist - Không khả dụng
/rmshare - Không khả dụng
/checkshare - Không khả dụng
/ext - Danh sách lệnh mở rộng
""", quote=True)

@Client.on_message(filters.command("ext"))
def ext_command_list(c, m):
  m.reply(f"""**{m.from_user.first_name}**(`{m.from_user.id}`), dưới đây là danh sách lệnh cấp cao:
/addpoint + `prefix` + `endpoint url` - Thêm điểm cuối cho thử nghiệm
/endpoints - Lấy danh sách điểm cuối và lệnh gọi
/delpoint + `prefix` - Xoá điểm cuối nếu nó thuộc về bạn
/install - Hướng dẫn cài điểm cuối 
/setupserver - Cài đặt điểm cuối tự động
/addserver - Thêm máy chủ SHH
/delserver - Xoá máy chủ SSH 
/machines - Danh sách máy chủ SSH đã thêm 
/cmd - Chạy lệnh shell trên máy chủ SSH
""", quote=True
)

@Client.on_message(filters.command("install"))
def help_install_endpoint(c, m):
  m.reply("""
Yêu cầu: Docker runtime(Máy tính, VPS...), cổng HTTP mở
Cài đặt: Sử dụng lệnh <pre> docker run -p 80:8080 ghcr.io/mymaking/test-endpoint:main </pre>. Có thể thay cổng 80 bằng cổng bất kỳ. 
Có thể sử dụng lệnh /setupserver để tự động cài đặt""", quote=True)

@Client.on_message(filters.command(["start","help"]))
def send_welcome(c, m):
  m.reply_text(f"Xin chào {m.from_user.first_name}(`{m.from_user.id}`)\n```Công cụ:\n{config_tool}```\nDùng lệnh /helps để biết thêm chi tiết", quote=True)