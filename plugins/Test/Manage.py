from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from lib.lite import get_endpoints
import os 
import time

@Client.on_message(filters.command("setpoint") & filters.user(5665225938))
def set_local_endpoint(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    try:
        if len(m.command) > 1:
            os.environ["ENDPOINT"] = m.command[1]
            st = m.reply("Đã chuyển đổi địa điểm test mặc định")
        else:
            os.environ["ENDPOINT"] = ""
            st = m.reply("Đã khôi phục địa điểm test mặc định")
    except Exception as e:
        st = m.reply(f"Lỗi: {e}", quote=True)
    time.sleep(20)
    st.delete()

@Client.on_message(filters.command("testservers"))
def list_endpoints(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    m.reply("Test trong trình duyệt: http://eu4.diresnode.com:3305/", quote=True)
    return 
    try:
            count, ___, endpoints = get_endpoints()
    except Exception as e:
            m.reply(str(e), quote=True)
            return
    endpoints = "\n".join(endpoints)
    echo = f"**Danh sách địa điểm test:({count})**\n\n"
    text = f"{echo}{endpoints}"
    m.reply(text, quote=True)
    
@Client.on_message(filters.command("addpoint"))
def add_endpoint(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    m.reply("Hệ thống địa điểm test mới, /install để biết cách cài đặt", quote=True)
    return
#     try:
#         if len(m.command) < 3:
#             raise Exception("Vui lòng làm theo mẫu để thêm máy chủ test\n```guide\n/addpoint + prefix + url\nví dụ: /addpoint vn http://103.0.0.0:80\n```")
#         prefix = m.command[1]
#         if len(prefix) > 20:
#             raise Exception("Tối đa là 20 ký tự. Vui lòng thử lại")
#         endpoint = m.command[2]
#         if not endpoint.startswith("http"):
#             raise Exception("Chỉ chấp nhận giao thức http/https")
#             return
#         sponsor = m.from_user.first_name
#         sponsor_id = m.from_user.id
#         if len(m.command) > 3:
#                 sponsor = m.command[3]
#         ep.add(sponsor, sponsor_id, prefix, endpoint)
#         st = m.reply(f"**{m.from_user.first_name}** đã thêm máy chủ test {prefix.upper()}", quote=True)
#     except Exception as e:
#         st = m.reply(f"```Lỗi:\n{e}\n```", quote=True)
#     time.sleep(20)
#     st.delete
#     m.delete()
    
@Client.on_message(filters.command("delpoint"))
def remove_endpoint(c, m):
        m.reply("Để xoá địa điểm test, hãy đóng chương trình trên máy chủ đó", quote=True)

#     try:
#         if len(m.command) < 2:
#             raise Exception("Vui lòng cung cấp prefix máy chủ test cần xoá")
#         prefix = m.command[1]
#         uid = m.from_user.id
#         _, sid, __ = ep.get(prefix)
#         if uid not in [int(sid), 5665225938]:
#             raise Exception("Máy chủ test này không thuộc sở hữu của bạn, không thể hoàn thành thao tác xoá")
#         ep.rm(prefix)
#         st = m.reply(f"Đã xoá máy chủ test **{prefix.upper()}**", quote=True)
#     except:
#         st = m.reply(f"Lỗi: {e}", quote=True)
#     time.sleep(20)
#     st.delete()
#     m.delete()