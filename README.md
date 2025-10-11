# SSH Remote Command Tool

Một tool đơn giản với giao diện web để thực thi các lệnh trên server remote qua SSH.

## Tính năng

- Giao diện web thân thiện và đẹp mắt
- **Unified Bash Execution**: Tất cả commands và scripts đều chạy dưới bash wrapper
- **Hai chế độ thực thi:**
  - **Bash Command**: Lệnh đơn lẻ được wrap trong bash script với verbose logging
  - **Custom Script**: Script phức tạp (Bash, Python, Shell) với detailed execution tracking
- **Advanced Verbose Logging**: 
  - `set -x`: Hiển thị từng command được execute
  - Capture tất cả stdout/stderr trong một output stream
  - Chi tiết execution flow của từng bước
- Kết nối SSH với private key (.pem)
- **Phân loại kết quả thông minh:**
  - ✅ **Success**: Exit code = 0
  - ⚠️ **Warning**: Exit code ≠ 0 
  - ❌ **Fail**: Không thể kết nối SSH
- Hiển thị original content + detailed bash execution log
- Real-time status updates
- Auto cleanup script files trên remote server

## Cài đặt

1. Cài đặt Python dependencies:
```bash
pip install flask paramiko
```

2. Chạy ứng dụng:
```bash
python app.py
```

3. Mở trình duyệt và truy cập: http://localhost:8080

## Sử dụng

1. **Host/IP Address**: Địa chỉ IP của server remote (ví dụ: 47.236.162.79)
2. **Port**: Port SSH (mặc định: 22)
3. **Username**: Tên user để đăng nhập (ví dụ: root, ubuntu)
4. **Private Key Path**: Đường dẫn đến file private key (.pem)
5. **Chọn chế độ**:
   - **Bash Command**: Lệnh sẽ được wrap trong bash script với verbose logging
   - **Custom Script**: Script tùy chỉnh (Bash, Python, Shell)

### Ví dụ Bash Command

**Input:**
```bash
ls -la && df -h && whoami
```

**Actual execution (auto-wrapped):**
```bash
#!/bin/bash
set -x
echo "=== EXECUTING COMMAND ==="
ls -la && df -h && whoami
echo "=== COMMAND COMPLETED ==="
```

**Output bạn sẽ thấy:**
```
=== ORIGINAL CONTENT ===
ls -la && df -h && whoami

=== BASH EXECUTION LOG ===
+ echo '=== EXECUTING COMMAND ==='
=== EXECUTING COMMAND ===
+ ls -la && df -h && whoami
total 24
drwxr-xr-x 3 root root 4096 Aug 24 10:30 .
drwxr-xr-x 4 root root 4096 Aug 24 10:30 ..
-rw-r--r-- 1 root root  220 Aug 24 10:30 .bashrc
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        20G  8.5G   11G  45% /
root
+ echo '=== COMMAND COMPLETED ==='
=== COMMAND COMPLETED ===
```

### Ví dụ Custom Script

**Python Script sẽ được wrap:**
```bash
#!/bin/bash
set -x
set -e
echo "=== EXECUTING PYTHON SCRIPT ==="
python3 -u << 'EOF'
import os
print(f"Current dir: {os.getcwd()}")
print("Files:")
for f in os.listdir('.'):
    print(f" - {f}")
EOF
echo "=== PYTHON SCRIPT COMPLETED ==="
```

## Lưu ý bảo mật

- Đảm bảo file private key có quyền phù hợp (chmod 600)
- Không chia sẻ private key với người khác
- Tool chạy trên localhost, không expose ra internet
- Các thông tin SSH không được lưu trữ lâu dài

## Troubleshooting

1. **Lỗi kết nối SSH**: 
   - Kiểm tra IP/port có đúng không
   - Kiểm tra private key có đúng format và quyền truy cập
   - Kiểm tra firewall có block port 22 không

2. **Lỗi permission denied**:
   - Kiểm tra username có đúng không
   - Kiểm tra private key có match với public key trên server không

3. **Command timeout**:
   - Các lệnh dài sẽ chạy trong background thread
   - Trang web sẽ poll kết quả mỗi giây
# Smart terminal
echo 'alias st="python3 ~/smart-terminal.py"' >> ~/.bashrc
source ~/.bashrc

# Giờ chỉ cần gõ
st
