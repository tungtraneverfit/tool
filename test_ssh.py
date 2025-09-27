#!/usr/bin/env python3
import requests
import json
import time

# Thông tin SSH từ câu lệnh của bạn: ssh -i ~/Downloads/test.pem root@47.236.162.79
test_data = {
    "host": "47.236.162.79",
    "username": "root",
    "key_path": "~/Downloads/test.pem",
    "command": "ls -la",
    "port": 22,
}


def test_ssh_command():
    print("🚀 Testing SSH Remote Command Tool...")
    print(f"📡 Host: {test_data['host']}")
    print(f"👤 User: {test_data['username']}")
    print(f"🔑 Key: {test_data['key_path']}")
    print(f"⚡ Command: {test_data['command']}")
    print("-" * 50)

    try:
        # Gửi request để thực thi command
        print("📤 Sending execute request...")
        response = requests.post(
            "http://localhost:8080/execute",
            json=test_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return

        result = response.json()
        command_id = result["command_id"]
        print(f"✅ Command submitted with ID: {command_id}")

        # Poll for results
        print("⏳ Waiting for results...")
        max_attempts = 30  # 30 seconds timeout
        attempt = 0

        while attempt < max_attempts:
            time.sleep(1)
            attempt += 1

            try:
                result_response = requests.get(
                    f"http://localhost:8080/result/{command_id}"
                )
                if result_response.status_code != 200:
                    print(f"❌ Error getting result: {result_response.status_code}")
                    continue

                result_data = result_response.json()
                status = result_data.get("status")

                if status == "running":
                    print(f"⏸️  Still running... ({attempt}s)")
                    continue

                elif status == "completed":
                    print("✅ Command completed successfully!")
                    print(f"Exit status: {result_data.get('exit_status')}")
                    print("-" * 30 + " OUTPUT " + "-" * 30)

                    if result_data.get("output"):
                        print("📄 STDOUT:")
                        print(result_data["output"])

                    if result_data.get("error"):
                        print("⚠️  STDERR:")
                        print(result_data["error"])

                    print("-" * 67)
                    return

                elif status == "error":
                    print(f"❌ Command failed: {result_data.get('error')}")
                    return

                else:
                    print(f"❓ Unknown status: {status}")
                    return

            except requests.exceptions.RequestException as e:
                print(f"❌ Network error: {e}")
                continue

        print("⏰ Timeout - command took too long to complete")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    test_ssh_command()
