# Test Script - Fail Fast Behavior

## Test Commands that Should Fail Fast

### Test Case 1: Multi-command với một command fail
```bash
cd ~/
ls -la
cd app
cat ngu.sh
echo "This should NOT execute"
```

### Expected Behavior with set -e:
- `cd ~/` ✅ success 
- `ls -la` ✅ success
- `cd app` ❌ fail (nếu folder không tồn tại)
- Script STOPS here, không chạy `cat ngu.sh` và `echo`
- Exit code != 0 → Status = WARNING

### Test Case 2: Command đơn fail
```bash
cat /nonexistent/file.txt
```

### Expected Behavior:
- Command fail ngay
- Exit code != 0 → Status = WARNING  
- Thấy error message trong log

### Test Case 3: Pipeline command
```bash
ls /nonexistent | grep test
```

### Expected Behavior với set -o pipefail:
- `ls /nonexistent` fails
- Entire pipeline fails 
- Exit code != 0 → Status = WARNING

## Testing Instructions:

1. Mở http://localhost:8080
2. Tab "💻 Bash Command" 
3. Nhập test case từ trên
4. Verify rằng:
   - Script dừng ngay khi có lỗi
   - Exit code đúng
   - Status hiển thị WARNING thay vì COMPLETED
   - Log shows exact command nào fail
