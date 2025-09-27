# 🐳 SSH Remote Command Tool - Docker Setup

## Cách sử dụng với Docker

### 1. Build Docker Image

```bash
# Cách 1: Sử dụng script build
./build.sh

# Cách 2: Build thủ công
docker build -t ssh-remote-tool .
```

### 2. Chạy với Docker Compose (Khuyến nghị)

```bash
# Chạy container
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng container
docker-compose down
```

### 3. Chạy với Docker run

```bash
docker run -d \
  --name ssh-remote-tool \
  -p 8080:8080 \
  -v ~/.ssh:/app/keys:ro \
  -v ~/Downloads:/app/downloads:ro \
  ssh-remote-tool
```

### 4. Truy cập ứng dụng

- **Web Interface**: http://localhost:8080
- **Container logs**: `docker-compose logs -f`
- **Stop container**: `docker-compose down`

### 5. Cấu hình SSH Keys trong Container

Ứng dụng mount 2 thư mục từ host:

- `~/.ssh` → `/app/keys` (read-only)
- `~/Downloads` → `/app/downloads` (read-only)

**Trong web interface, sử dụng đường dẫn:**
- `/app/keys/id_rsa` (cho SSH key từ ~/.ssh)
- `/app/downloads/test.pem` (cho key từ ~/Downloads)

### 6. Ví dụ sử dụng

**Thông tin nhập vào web:**
- **Host**: `47.236.162.79`
- **Username**: `root`
- **Key Path**: `/app/downloads/test.pem`
- **Command**: `ls -la`

### 7. Troubleshooting

```bash
# Kiểm tra container đang chạy
docker ps

# Xem logs chi tiết
docker-compose logs ssh-tool

# Vào bên trong container để debug
docker exec -it ssh-remote-tool bash

# Kiểm tra file permissions
docker exec ssh-remote-tool ls -la /app/keys
docker exec ssh-remote-tool ls -la /app/downloads
```

### 8. Bảo mật

- Container chạy với user non-root
- SSH keys được mount read-only
- Không có SSH keys nào được copy vào image
- Health check tự động kiểm tra ứng dụng

### 9. Customization

**Thay đổi port:**
```yaml
# Trong docker-compose.yml
ports:
  - "3000:8080"  # Chạy trên port 3000
```

**Mount thêm thư mục khác:**
```yaml
volumes:
  - ~/my-keys:/app/my-keys:ro
```
