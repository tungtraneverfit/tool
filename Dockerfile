# Sử dụng Python 3.11 slim image
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các dependencies hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    openssh-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file trước để tận dụng Docker cache
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Tạo thư mục cho SSH keys (optional)
RUN mkdir -p /app/keys

# Expose port 8080
EXPOSE 8080

# Tạo user non-root để chạy app an toàn hơn
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Command để chạy app
CMD ["python", "app.py"]
