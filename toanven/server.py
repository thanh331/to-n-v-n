import socket
import hashlib
import os

HOST = '0.0.0.0' # Lắng nghe trên tất cả các địa chỉ mạng có sẵn
PORT = 12345     # Cổng riêng biệt cho server socket, khác với Flask (5000)
BUFFER_SIZE = 4096
SAVE_FOLDER = 'received_files'
os.makedirs(SAVE_FOLDER, exist_ok=True) # Đảm bảo thư mục lưu trữ tồn tại

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1) # Chấp nhận một kết nối tại một thời điểm
print(f"[*] Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept() # Chấp nhận kết nối từ client
    print(f"[+] {addr} connected.")

    try:
        # Nhận tên file từ client
        filename = conn.recv(BUFFER_SIZE).decode()
        conn.send(b'FILENAME RECEIVED') # Gửi xác nhận đã nhận tên file

        # Nhận dữ liệu file
        file_data = b''
        while True:
            chunk = conn.recv(BUFFER_SIZE)
            if chunk == b'EOF': # Client gửi "EOF" để báo hiệu kết thúc file
                break
            file_data += chunk

        # Nhận hash của file từ client
        hash_received = conn.recv(BUFFER_SIZE).decode()

        # Lưu file đã nhận
        file_path = os.path.join(SAVE_FOLDER, filename)
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Tính toán hash của file đã nhận và so sánh
        sha256_hash = hashlib.sha256(file_data).hexdigest()
        if sha256_hash == hash_received:
            print(f"[+] File received intact: {filename}")
            conn.send(b"RESULT: OK")
        else:
            print(f"[!] File corrupted: {filename}")
            conn.send(b"RESULT: FAILED")
    except Exception as e:
        print(f"[-] Error during file transfer: {e}")
        conn.send(b"ERROR during transfer") # Gửi thông báo lỗi cho client
    finally:
        conn.close() # Đóng kết nối