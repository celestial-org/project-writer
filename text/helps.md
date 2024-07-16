__Xin chào **{first_name}**(`{uid}`), dưới đây là danh sách lệnh khả dụng:__

**Rewriting**

/test - Kiểm tra cấu hình v2ray...

/checks - Kiểm tra subscription

/filter_alive - Lọc ra server còn khả dụng từ subscription

**Note Writing**
    
/get - Lấy liên kết note **share**

/add - Thêm subscription vào note/thêm vào note **share** nếu không chỉ định tên note

/share - Chia sẻ subscription/thêm vào note **share**

/note - Kiểm tra danh sách link trong note chỉ định (yêu cầu quyền truy cập), có thể chỉ định `share"` để truy cập note **share**

/delete - Xoá subscription khỏi note chỉ định (yêu cầu quyền truy cập)

/check_alive - Tự kiểm tra và xoá subscription bị lỗi (không bao gồm subscribe hết lưu lượng truy cập)

/deleteshare - Xoá subscription khỏi danh sách chia sẻ 

/check_share - Kiểm tra và xoá subscription bị lỗi khỏi danh sách chia sẻ

**Khác**

/request [get, post, put, delete, option] - Gửi yêu cầu HTTP/HTTPS

/ext - Các lệnh nâng cao