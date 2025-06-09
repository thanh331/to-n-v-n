<h1>Bảo mật và toàn vẹn</h1>
<img src="" alt="Đăng nhập để tiếp tục">
<p>🔐 Chức năng 1: Xác thực người dùng
Giao diện web có form đăng nhập.

Mã backend (app.py) kiểm tra tên người dùng và mật khẩu từ một dictionary users.

Sau khi đăng nhập thành công, thông tin người dùng được lưu trong session.

📤 Chức năng 2: Tải tệp lên (Upload)
Người dùng đã đăng nhập có thể tải lên tệp đến người dùng khác.

File được lưu trong thư mục uploads/<tên người nhận>.

Hệ thống tính mã băm SHA-256 của file để đảm bảo tính toàn vẹn.

Trả về mã SHA-256 sau khi upload thành công.

📥 Chức năng 3: Xem và tải tệp về
Người dùng có thể liệt kê các tệp đã nhận.

Cho phép tải về tệp đã gửi đến đúng người nhận (có kiểm tra quyền truy cập).

Tệp được gửi kèm dưới dạng file đính kèm (as_attachment=True).

🧾 Chức năng 4: Đăng xuất
Gọi /logout để kết thúc phiên người dùng hiện tại.

🖥️ Chức năng 5: Giao tiếp qua Socket (server.py)
Server riêng (server.py) lắng nghe trên cổng 12345 để nhận tệp từ client qua TCP socket.

Nhận tên file, nội dung file và mã SHA-256 từ client.

So sánh hash tính được với hash nhận được để kiểm tra tính toàn vẹn.

Lưu tệp vào thư mục received_files nếu hợp lệ.</p>
