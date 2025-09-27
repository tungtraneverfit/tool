#!/usr/bin/env python3
"""
Demo trực tiếp SSH command với thông tin bạn cung cấp
Thay thế cho việc test qua web interface
"""
import paramiko
import os


def test_ssh_direct():
    print("🔑 Testing SSH connection directly...")
    print("=" * 50)

    # Thông tin từ câu lệnh: ssh -i ~/Downloads/test.pem root@47.236.162.79
    host = "47.236.162.79"
    username = "root"
    key_path = os.path.expanduser("~/Downloads/test.pem")
    command = "ls -la"
    port = 22

    print(f"📡 Host: {host}")
    print(f"👤 User: {username}")
    print(f"🔑 Key: {key_path}")
    print(f"⚡ Command: {command}")
    print("-" * 50)

    # Kiểm tra file key có tồn tại không
    if not os.path.exists(key_path):
        print(f"❌ Private key file not found: {key_path}")
        print("💡 Tip: Đảm bảo file key.pem có tồn tại ở đường dẫn đúng")
        return False

    # Kiểm tra quyền file
    file_mode = oct(os.stat(key_path).st_mode)[-3:]
    print(f"🔒 Key file permissions: {file_mode}")

    if file_mode != "600":
        print("⚠️  Warning: Key file should have 600 permissions")
        print(f"   Run: chmod 600 {key_path}")

    try:
        print("🔄 Attempting SSH connection...")

        # Tạo SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load private key
        try:
            if key_path.endswith(".pem"):
                private_key = paramiko.RSAKey.from_private_key_file(key_path)
            else:
                private_key = paramiko.RSAKey.from_private_key_file(key_path)
            print("✅ Private key loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load private key: {e}")
            return False

        # Kết nối SSH
        ssh.connect(
            hostname=host, port=port, username=username, pkey=private_key, timeout=10
        )
        print("✅ SSH connection established")

        # Thực thi lệnh
        print(f"⚡ Executing: {command}")
        stdin, stdout, stderr = ssh.exec_command(command)

        # Đọc kết quả
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        exit_status = stdout.channel.recv_exit_status()

        ssh.close()

        print("🎉 Command executed successfully!")
        print(f"Exit status: {exit_status}")
        print("=" * 30 + " OUTPUT " + "=" * 30)

        if output:
            print("📄 STDOUT:")
            print(output)

        if error:
            print("⚠️  STDERR:")
            print(error)

        print("=" * 67)
        return True

    except paramiko.AuthenticationException:
        print("❌ Authentication failed")
        print("💡 Check if the private key matches the public key on server")
        return False
    except paramiko.SSHException as e:
        print(f"❌ SSH error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = test_ssh_direct()
    if success:
        print("\n✅ SSH tool is working correctly!")
        print("🌐 You can now use the web interface at: http://localhost:8080")
    else:
        print("\n❌ SSH connection failed")
        print("🔧 Please check your SSH credentials and network connectivity")
