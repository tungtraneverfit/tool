from flask import Flask, render_template, request, jsonify, Response
import paramiko
import os
import threading
import time
import tempfile
import uuid
import json
import queue

app = Flask(__name__)

# Store for command results
results = {}

# Store for streaming logs
stream_queues = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/execute", methods=["POST"])
def execute_command():
    data = request.get_json()

    host = data.get("host")
    username = data.get("username")
    key_path = data.get("key_path")
    command = data.get("command")
    script_content = data.get("script_content")
    script_type = data.get("script_type", "bash")  # bash, python, sh
    port = data.get("port", 22)

    if not all([host, username, key_path]):
        return jsonify({"error": "Thiếu thông tin host, username hoặc key_path"}), 400

    if not command and not script_content:
        return jsonify({"error": "Cần nhập ít nhất command hoặc script"}), 400

    # Tạo ID duy nhất cho command này
    command_id = f"{int(time.time() * 1000)}"

    # Tạo queue cho streaming
    stream_queue = queue.Queue()
    stream_queues[command_id] = stream_queue

    # Chạy command trong thread riêng
    def run_ssh_command():
        import time

        start_time = time.time()

        def stream_log(message):
            """Helper function to stream log messages"""
            try:
                stream_queue.put(
                    {"type": "log", "message": message, "timestamp": time.time()}
                )
            except:
                pass

        try:
            stream_log("🔗 Đang kết nối SSH...")

            # Kết nối SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Load private key
            if key_path.endswith(".pem"):
                private_key = paramiko.RSAKey.from_private_key_file(key_path)
            else:
                private_key = paramiko.RSAKey.from_private_key_file(key_path)

            ssh.connect(hostname=host, port=port, username=username, pkey=private_key)
            stream_log(f"✅ Kết nối SSH thành công tới {host}")

            # Xử lý script hoặc command - tất cả đều chạy dưới dạng bash script
            script_filename = f"/tmp/script_{uuid.uuid4().hex[:8]}.sh"

            if script_content:
                # Script mode: sử dụng script content với script type được chọn
                if script_type == "python":
                    # Python script: wrap trong bash để có verbose logging
                    python_content = script_content
                    full_script = f"""#!/bin/bash
set -x
set -e
set -o pipefail
echo "=== EXECUTING PYTHON SCRIPT ==="
python3 -u << 'EOF'
{python_content}
EOF
echo "=== PYTHON SCRIPT COMPLETED ==="
"""
                else:
                    # Bash hoặc sh script: thêm verbose flags
                    full_script = f"""#!/bin/bash
set -x
set -e
set -o pipefail
echo "=== EXECUTING {script_type.upper()} SCRIPT ==="
{script_content}
echo "=== SCRIPT COMPLETED ==="
"""
                display_command = f"[SCRIPT {script_type.upper()}]\n{script_content}"

            else:
                # Command mode: wrap command trong bash script
                full_script = f"""#!/bin/bash
set -x
set -e
set -o pipefail
echo "=== EXECUTING COMMAND ==="
{command}
echo "=== COMMAND COMPLETED ==="
"""
                display_command = f"[BASH WRAPPED COMMAND]\n{command}"

            # Upload script lên server
            stream_log("📤 Đang upload script lên server...")
            sftp = ssh.open_sftp()
            with sftp.open(script_filename, "w") as f:
                f.write(full_script)
            sftp.close()

            # Cấp quyền thực thi
            ssh.exec_command(f"chmod +x {script_filename}")
            stream_log("⚙️ Đã cấp quyền thực thi cho script")

            # Chạy script trực tiếp (đã có set -x trong script)
            final_command = f"{script_filename}"
            stream_log(f"🚀 Bắt đầu thực thi: {display_command.split(chr(10))[0]}")

            # Thực thi command/script với combined output và streaming
            stdin, stdout, stderr = ssh.exec_command(f"{final_command} 2>&1")

            # Đọc output theo dòng để streaming real-time
            output_lines = []
            while True:
                line = stdout.readline()
                if not line:
                    break
                line = line.rstrip("\n\r")
                if line:
                    output_lines.append(line)
                    stream_log(line)

            # Lấy exit status
            exit_status = stdout.channel.recv_exit_status()
            output = "\n".join(output_lines)
            error = ""  # Đã combined vào output

            # Xóa script tạm nếu có
            if script_content:
                ssh.exec_command(f"rm -f {script_filename}")
                stream_log("🧹 Đã xóa script tạm")

            ssh.close()
            stream_log("🔌 Đã đóng kết nối SSH")

            # Tính thời gian thực thi
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)

            # Phân loại kết quả dựa trên exit code
            if exit_status == 0:
                status = "completed"
                status_message = f"✅ Thực thi thành công trong {execution_time}s"
                stream_log(
                    f"✅ Hoàn thành thành công! (Exit code: {exit_status}, Time: {execution_time}s)"
                )
            else:
                status = "warning"  # Exit code != 0 là warning
                status_message = f"⚠️ Thực thi có lỗi trong {execution_time}s (exit code: {exit_status})"
                stream_log(
                    f"⚠️ Hoàn thành với lỗi! (Exit code: {exit_status}, Time: {execution_time}s)"
                )

            results[command_id] = {
                "status": status,
                "output": output,
                "error": error,
                "exit_status": exit_status,
                "command": display_command,
                "host": host,
                "type": "script" if script_content else "bash_command",
                "execution_time": execution_time,
                "status_message": status_message,
            }

            # Signal stream completion
            stream_queue.put(
                {
                    "type": "complete",
                    "status": status,
                    "execution_time": execution_time,
                    "exit_status": exit_status,
                }
            )

        except Exception as e:
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)

            error_msg = f"❌ Lỗi kết nối: {str(e)}"
            stream_log(error_msg)

            results[command_id] = {
                "status": "fail",  # Không connect được là fail
                "error": str(e),
                "command": script_content if script_content else command,
                "host": host,
                "type": "script" if script_content else "bash_command",
                "execution_time": execution_time,
                "status_message": f"❌ Kết nối thất bại sau {execution_time}s: {str(e)}",
            }

            # Signal stream completion with error
            stream_queue.put(
                {
                    "type": "complete",
                    "status": "fail",
                    "execution_time": execution_time,
                    "error": str(e),
                }
            )

    # Khởi tạo result
    results[command_id] = {
        "status": "running",
        "command": script_content if script_content else command,
        "host": host,
        "type": "script" if script_content else "bash_command",
    }

    # Chạy command trong thread riêng
    thread = threading.Thread(target=run_ssh_command)
    thread.daemon = True
    thread.start()

    return jsonify({"command_id": command_id})


@app.route("/result/<command_id>")
def get_result(command_id):
    if command_id in results:
        return jsonify(results[command_id])
    else:
        return jsonify({"error": "Command ID không tồn tại"}), 404


@app.route("/stream/<command_id>")
def stream_logs(command_id):
    """Server-Sent Events endpoint for streaming logs"""

    def generate():
        if command_id not in stream_queues:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Command ID không tồn tại'})}\n\n"
            return

        stream_queue = stream_queues[command_id]

        try:
            while True:
                try:
                    # Đợi message từ queue với timeout
                    message = stream_queue.get(timeout=30)  # 30 second timeout

                    # Send message to client
                    yield f"data: {json.dumps(message)}\n\n"

                    # Nếu là complete message thì kết thúc stream
                    if message.get("type") == "complete":
                        break

                except queue.Empty:
                    # Send keepalive message
                    yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
                    continue

        except GeneratorExit:
            # Client đã đóng connection
            pass
        finally:
            # Cleanup queue sau khi stream xong
            if command_id in stream_queues:
                try:
                    # Clear remaining messages
                    while not stream_queue.empty():
                        stream_queue.get_nowait()
                except:
                    pass
                del stream_queues[command_id]

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        },
    )


if __name__ == "__main__":
    import os

    debug_mode = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug_mode, host="0.0.0.0", port=8080)
