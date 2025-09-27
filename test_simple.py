#!/usr/bin/env python3
import requests
import json


# Test với một server demo (thay vì server thực của bạn)
def test_tool_interface():
    print("🧪 Testing tool interface...")

    # Test 1: Kiểm tra trang chính có load được không
    try:
        response = requests.get("http://localhost:8080/")
        if response.status_code == 200:
            print("✅ Web interface loaded successfully")
        else:
            print(f"❌ Web interface failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to web interface: {e}")
        return

    # Test 2: Kiểm tra API endpoint với thông tin giả
    test_data = {
        "host": "47.236.162.79",  # Server của bạn
        "username": "root",
        "key_path": "~/Downloads/test.pem",  # Đường dẫn key của bạn
        "command": "ls -la",
        "port": 22,
    }

    print("\n📡 Testing SSH execution endpoint...")
    print(f"Host: {test_data['host']}")
    print(f"User: {test_data['username']}")
    print(f"Key: {test_data['key_path']}")
    print(f"Command: {test_data['command']}")

    try:
        response = requests.post(
            "http://localhost:8080/execute",
            json=test_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Command submitted successfully")
            print(f"Command ID: {result.get('command_id')}")

            # Thông báo kết quả
            print("\n📝 Note: Tool is working! Results depend on:")
            print("  - SSH server accessibility")
            print("  - Private key file existence and permissions")
            print("  - Network connectivity")
            print(
                "\nCheck the web interface at http://localhost:8080 for real-time results!"
            )

        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ API test failed: {e}")


if __name__ == "__main__":
    test_tool_interface()
