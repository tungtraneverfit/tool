# Test Script Examples for Verbose Logging

## Bash Script với lỗi để test logging:

```bash
echo "Starting script execution..."
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"

# Command thành công
ls -la /tmp

echo "Running a command that will fail..."
# Command sẽ fail
ls -la /nonexistent_directory

echo "This line might not execute if set -e is enabled"
```

## Python Script với lỗi để test logging:

```python
print("Starting Python script...")
import os
import sys

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Code thành công
print("Files in current directory:")
for f in os.listdir('.'):
    print(f" - {f}")

print("Attempting to read non-existent file...")
# Code sẽ có lỗi
try:
    with open('/nonexistent_file.txt', 'r') as f:
        content = f.read()
        print(content)
except FileNotFoundError as e:
    print(f"Error: {e}")

print("Script completed")
```

## Expected Output:

### Với verbose logging, bạn sẽ thấy:

1. **SCRIPT CONTENT**: Nội dung script bạn viết
2. **EXECUTION LOG**: 
   - Với Bash: `set -x` sẽ show từng command được execute (+ command)
   - Với Python: Output từng dòng của script
3. **ERROR LOG**: Chi tiết lỗi nếu có

### Ví dụ output với Bash script có lỗi:
```
=== SCRIPT CONTENT ===
echo "Starting script execution..."
ls -la /nonexistent_directory

=== EXECUTION LOG ===
+ echo 'Starting script execution...'
Starting script execution...
+ ls -la /nonexistent_directory
ls: cannot access '/nonexistent_directory': No such file or directory

=== ERROR LOG ===
(Any stderr output here)
```

Status sẽ là **WARNING** vì exit code != 0, nhưng bạn vẫn thấy được chi tiết log của từng bước.
