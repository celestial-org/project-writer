from pyrogram import Client, filters

@Client.on_message(filters.command("help") & (filters.mentioned|filters.private))
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
/killpoint + `prefix` - Xoá điểm cuối nếu nó thuộc về bạn
/future - ....
""", quote=True
)