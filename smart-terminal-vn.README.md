# 🚀 Smart Terminal

**Terminal Thông Minh với Gợi Ý Lệnh Thời Gian Thực & Tích Hợp Git**

Một terminal hiện đại, mạnh mẽ với gợi ý lệnh thông minh, tích hợp git và prompt đẹp mắt - giống Oh My Zsh nhưng thông minh hơn!

[🇻🇳 Tiếng Việt](#) | [🇺🇸 English](README_EN.md)

## 🌟 Tính năng

### 🧠 **Gợi ý thông minh**
- **Gợi ý theo thời gian thực** khi bạn gõ
- **Hiểu ngữ cảnh** để đưa ra gợi ý phù hợp  
- **Hệ thống ưu tiên đa cấp** với 6 mức độ thông minh
- **Tab cycling** để duyệt qua các loại gợi ý

### 🎨 **Prompt đẹp với tích hợp Git**
```bash
# Repository sạch
(username)directory git:(master)$ 

# Có thay đổi
(username)directory git:(feature)$ 
```
- **Chữ in đậm** để dễ nhìn hơn
- **Hiển thị git branch** với màu sắc theo trạng thái:
  - 🟢 Green: Clean repository
  - 🟡 Yellow: Staged changes
  - 🔴 Red: Unstaged/untracked changes

#### 📚 **Rich Command Database**
- **1000+ built-in commands** for Git, Docker, Node.js, Python, Linux
- **Smart file completion** based on command context
- **Auto-learning** from your usage history

#### ⌨️ **Advanced Navigation**
- **↑/↓ Arrow keys** to browse command history
- **Tab/→** to accept suggestions
- **Ctrl+C** safe handling without corrupting history

#### 🔗 **System Integration**
- **Seamless history sync** with your shell (bash/zsh)
- **Cross-session** command sharing
- **Safe command truncation** for long commands

### 🚀 Quick Start

```bash
# Clone or download
git clone <repository-url>
cd smart-terminal

# Run normally
python3 smart-terminal.py

# Run with timing mode
python3 smart-terminal.py -t
```

### 🎮 Usage

#### Basic Commands
```bash
# Type and see suggestions
git st[TAB] → git status

# Navigate history
↑ → Previous commands
↓ → Next commands

# Special commands
history    # Show command history
stats      # Usage statistics
clear      # Clear screen
exit       # Quit terminal
```

#### Tab Cycling System
```bash
python[TAB]           # → "python " (add space)
python [TAB]          # → "python script.py" (Python files)
python [TAB][TAB]     # → "python app.py" (next Python file)
```

### � Priority System

1. **🏆 Aliases** (highest) - `mk` → `mkdir`
2. **⚡ Command Completion** - `git` → `git `
3. **📁 Smart File Completion** - `python ` → `python script.py`
4. **📚 Database Suggestions** - `git ` → `git status`
5. **🔍 Fuzzy Search** - All database commands
6. **📜 History** (lowest) - Previous commands

### � Advanced Features

#### Timing Mode
```bash
python3 smart-terminal.py -t
```
- Shows execution time for each command
- Color-coded performance indicators

#### Smart File Completion
- **Python commands**: Show only `.py` files
- **Node commands**: Show only `.js` files  
- **Git commands**: Show appropriate files/directories

#### Customizable Aliases
Built-in shortcuts:
- `so` → `source`
- `mk` → `mkdir`
- `his` → `history`

### �️ Customization

Add custom aliases in `smart-terminal.py`:
```python
self.aliases = {
    "so": "source",
    "mk": "mkdir",
    "ll": "ls -la",     # Add your own
    "gs": "git status"  # Add your own
}
```

---

## Tiếng Việt

### 🌟 Tính năng

#### 🧠 **Gợi ý thông minh**
- **Gợi ý theo thời gian thực** khi bạn gõ
- **Hiểu ngữ cảnh** để đưa ra gợi ý phù hợp  
- **Hệ thống ưu tiên đa cấp** với 6 mức độ thông minh
- **Tab cycling** để duyệt qua các loại gợi ý

#### 🎨 **Prompt đẹp với tích hợp Git**
```bash
# Repository sạch
(username)directory git:(master)$ 

# Có thay đổi
(username)directory git:(feature)$ 
```
- **Chữ in đậm** để dễ nhìn hơn
- **Hiển thị git branch** với màu sắc theo trạng thái:
  - 🟢 Xanh: Repository sạch sẽ
  - 🟡 Vàng: Có staged changes
  - 🔴 Đỏ: Có unstaged/untracked changes

#### 📚 **Cơ sở dữ liệu lệnh phong phú**
- **1000+ lệnh có sẵn** cho Git, Docker, Node.js, Python, Linux
- **Gợi ý file thông minh** dựa trên ngữ cảnh lệnh
- **Tự học** từ lịch sử sử dụng của bạn

#### ⌨️ **Điều hướng nâng cao**
- **Phím ↑/↓** để duyệt lịch sử lệnh
- **Tab/→** để chấp nhận gợi ý
- **Ctrl+C** xử lý an toàn không làm hỏng history

#### 🔗 **Tích hợp hệ thống**
- **Đồng bộ history** mượt mà với shell (bash/zsh)
- **Chia sẻ lệnh** giữa các session
- **Cắt ngắn lệnh dài** một cách an toàn

### 🚀 Bắt đầu nhanh

```bash
# Clone hoặc tải về
git clone <repository-url>
cd smart-terminal

# Chạy bình thường
python3 smart-terminal.py

# Chạy với chế độ timing
python3 smart-terminal.py -t
```

### 🎮 Cách sử dụng

#### Lệnh cơ bản
```bash
# Gõ và xem gợi ý
git st[TAB] → git status

# Điều hướng history
↑ → Lệnh trước đó
↓ → Lệnh tiếp theo

# Lệnh đặc biệt
history    # Xem lịch sử lệnh
stats      # Thống kê sử dụng
clear      # Xóa màn hình
exit       # Thoát terminal
```

#### Hệ thống Tab Cycling
```bash
python[TAB]           # → "python " (thêm space)
python [TAB]          # → "python script.py" (file Python)
python [TAB][TAB]     # → "python app.py" (file Python tiếp theo)
```

### 🎯 Hệ thống ưu tiên

1. **🏆 Aliases** (cao nhất) - `mk` → `mkdir`
2. **⚡ Hoàn thành lệnh** - `git` → `git `
3. **📁 Hoàn thành file thông minh** - `python ` → `python script.py`
4. **� Gợi ý từ database** - `git ` → `git status`
5. **🔍 Tìm kiếm mờ** - Tất cả lệnh trong database
6. **📜 Lịch sử** (thấp nhất) - Lệnh đã dùng trước đó

### 📊 Tính năng nâng cao

#### Chế độ Timing
```bash
python3 smart-terminal.py -t
```
- Hiển thị thời gian thực thi cho mỗi lệnh
- Chỉ báo hiệu suất bằng màu sắc

#### Hoàn thành file thông minh
- **Lệnh Python**: Chỉ hiện file `.py`
- **Lệnh Node**: Chỉ hiện file `.js`
- **Lệnh Git**: Hiện file/thư mục phù hợp

#### Aliases có thể tùy chỉnh
Shortcuts có sẵn:
- `so` → `source`
- `mk` → `mkdir`
- `his` → `history`

### 🛠️ Tùy chỉnh

Thêm aliases tùy chỉnh trong `smart-terminal.py`:
```python
self.aliases = {
    "so": "source",
    "mk": "mkdir",
    "ll": "ls -la",     # Thêm của bạn
    "gs": "git status"  # Thêm của bạn
}
```

### 🐛 Xử lý sự cố

#### Lỗi thường gặp

**1. Lệnh git branch không hiển thị**
```bash
# Kiểm tra git có hoạt động không
git --version
git status
```

**2. Terminal không hiển thị màu**
```bash
# Đảm bảo terminal hỗ trợ ANSI colors
echo -e "\033[32mGreen text\033[0m"
```

**3. History không load**
```bash
# Kiểm tra file history
ls -la ~/.smart_terminal_history
```

### 📈 Roadmap tương lai

- 🔍 **Fuzzy search nâng cao**: Tìm kiếm thông minh hơn
- 🤖 **AI suggestions**: Sử dụng AI để gợi ý
- 🌐 **Plugin system**: Hỗ trợ plugin bên thứ 3
- 📱 **Mobile support**: Hỗ trợ Termux Android
- 🔄 **Auto-update**: Tự động cập nhật database

### 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

### 🤝 Đóng góp

Rất welcome các contributions! Hãy tạo Pull Request nhé.

---

**Made with ❤️ for developers who love efficiency**
