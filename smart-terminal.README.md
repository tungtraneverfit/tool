# 🚀 Smart Terminal

**Intelligent Terminal with Real-time Autosuggestions & Git Integration**

A powerful, modern terminal replacement with smart command suggestions, git integration, and beautiful prompts - like Oh My Zsh but smarter!

## � Features

### 🧠 **Smart Autosuggestions**
- **Real-time suggestions** as you type
- **Context-aware** command completion
- **Multi-priority system** with 6 levels of intelligence
- **Tab cycling** through different suggestion types

### 🎨 **Beautiful Git-Integrated Prompt**
```bash
# Clean repository
(username)directory git:(master)$ 

# With changes
(username)directory git:(feature)$ 
```
- **Bold formatting** for better visibility
- **Git branch detection** with status colors:
  - 🟢 Green: Clean repository
  - 🟡 Yellow: Staged changes
  - 🔴 Red: Unstaged/untracked changes

### 📚 **Rich Command Database**
- **1000+ built-in commands** for Git, Docker, Node.js, Python, Linux
- **Smart file completion** based on command context
- **Auto-learning** from your usage history

### ⌨️ **Advanced Navigation**
- **↑/↓ Arrow keys** to browse command history
- **Tab/→** to accept suggestions
- **Ctrl+C** safe handling without corrupting history

### 🔗 **System Integration**
- **Seamless history sync** with your shell (bash/zsh)
- **Cross-session** command sharing
- **Safe command truncation** for long commands

## 🚀 Quick Start

```bash
# Clone or download
git clone <repository-url>
cd smart-terminal

# Run normally
python3 smart-terminal.py

# Run with timing mode
python3 smart-terminal.py -t
```

### System Requirements
- Python 3.6+
- macOS/Linux (Terminal environment)
- Bash or Zsh shell

## 🎮 Usage

### Basic Commands
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

### Tab Cycling System
```bash
python[TAB]           # → "python " (add space)
python [TAB]          # → "python script.py" (Python files)
python [TAB][TAB]     # → "python app.py" (next Python file)
```

### Built-in Aliases
```bash
so    # → source
mk    # → mkdir  
his   # → history
```

## 🎯 Priority System

1. **🏆 Aliases** (highest) - `mk` → `mkdir`
2. **⚡ Command Completion** - `git` → `git `
3. **📁 Smart File Completion** - `python ` → `python script.py`
4. **📚 Database Suggestions** - `git ` → `git status`
5. **🔍 Fuzzy Search** - All database commands
6. **📜 History** (lowest) - Previous commands

## 📊 Advanced Features

### Timing Mode
```bash
python3 smart-terminal.py -t
```
- Shows execution time for each command
- Color-coded performance indicators:
  - 🟢 < 1s: Green
  - 🟡 1-60s: Yellow  
  - 🔴 > 60s: Red

### Smart File Completion
- **Python commands**: Show only `.py` files
- **Node commands**: Show only `.js` files  
- **Git commands**: Show appropriate files/directories
- **C/C++ commands**: Show `.c`, `.cpp`, `.h` files

### Statistics
```bash
stats
```
Displays:
- Total commands executed
- Top 10 most used commands
- Detailed usage statistics

### Git Integration
- **Automatic branch detection** in git repositories
- **Status indicators** with color coding
- **Clean/dirty repository** visual feedback

## 🆚 Comparison with Regular Terminal

| Feature | Regular Terminal | Smart Terminal |
|---------|------------------|----------------|
| **Autosuggestion** | ❌ None | ✅ Real-time, intelligent |
| **Tab completion** | ⚡ Basic | 🚀 Multi-level, context-aware |
| **History** | 📝 Simple | 🧠 System integrated + learning |
| **Command database** | ❌ None | ✅ 1000+ built-in commands |
| **Visual feedback** | 🔲 Monochrome | 🎨 Colorful, informative |
| **Git integration** | ❌ None | ✅ Branch display in prompt |
| **File completion** | ⚡ Basic | 🎯 Smart filtering by command |
| **Cross-session** | ⚡ Limited | ✅ Full system sync |

## 🛠️ Customization

### Adding Custom Aliases
Edit `smart-terminal.py`:
```python
self.aliases = {
    "so": "source",
    "mk": "mkdir",
    "ll": "ls -la",     # Add your own
    "gs": "git status", # Add your own
    "dc": "docker-compose"
}
```

### Adding New Commands
Add to `suggestions_db`:
```python
"your-command": [
    "your-command --help",
    "your-command --version",
    "your-command start",
    "your-command stop"
]
```

### Custom Command Filters
Add file extensions for smart completion:
```python
"command_filters": {
    "python3": [".py"],
    "node": [".js", ".mjs"],
    "gcc": [".c", ".cpp", ".h"]
}
```

## 🐛 Troubleshooting

### Common Issues

**1. Git branch not showing**
```bash
# Check if git is working
git --version
git status

# Ensure you're in a git repository
git init  # If needed
```

**2. No color display**
```bash
# Ensure terminal supports ANSI colors
echo -e "\033[32mGreen text\033[0m"

# Check terminal type
echo $TERM
```

**3. History not loading**
```bash
# Check history file permissions
ls -la ~/.smart_terminal_history

# Check if file exists and is readable
chmod 644 ~/.smart_terminal_history
```

**4. ImportError or ModuleNotFoundError**
```bash
# Ensure Python 3.6+
python3 --version

# Run from correct directory
cd /path/to/smart-terminal
python3 smart-terminal.py
```

**5. Suggestions not working**
- Ensure running in a real terminal (not IDE)
- Terminal must support ANSI colors
- Check if `.smart_terminal_db.json` is created

## 🔧 Development

### Project Structure
```
smart-terminal/
├── smart-terminal.py      # Main application
├── README.md             # Vietnamese documentation
├── README_EN.md          # English documentation
├── test_suggestions.py   # Test file for suggestions
└── test_git.py          # Git detection test
```

### Testing
```bash
# Test suggestions
python3 test_suggestions.py

# Test git detection
python3 test_git.py

# Run with debug mode (modify code to enable)
python3 smart-terminal.py
```

## 📈 Future Roadmap

- 🔍 **Enhanced fuzzy search**: More intelligent search algorithms
- 🤖 **AI-powered suggestions**: Machine learning for better predictions
- 🌐 **Plugin system**: Support for third-party plugins
- 📱 **Mobile support**: Termux support for Android
- 🔄 **Auto-update**: Automatic command database updates
- 🌍 **Multi-language**: Support for more languages
- 🔐 **Security**: Enhanced security features for sensitive commands

## 📄 License

MIT License - Free to use for personal and commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes
4. **Push** to the branch
5. **Create** a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add tests for new features
- Update documentation for changes
- Ensure backward compatibility

## 💬 Support

- **Issues**: Report bugs and request features on GitHub
- **Documentation**: Check this README for common solutions
- **Community**: Join discussions and share your experience

---

**Made with ❤️ for developers who love efficiency**

*Transform your terminal experience today!*
# Clone or download smart-terminal.py
cd /path/to/smart-terminal

# Run in normal mode
python3 smart-terminal.py

# Run with timing mode (shows execution time)
python3 smart-terminal.py -t
```

### Exit
```bash
exit        # or
quit        # or
Ctrl+C      # or
Ctrl+D
```

## 🎮 How to Use

### 📝 **Basic Usage**
1. **Type command**: Start typing any command
2. **See suggestions**: Gray suggestions appear on the right
3. **Accept**: Press `Tab` or `→` to accept suggestion
4. **Execute**: Press `Enter` to run the command

### 🔄 **Tab Cycling**
```bash
touch<Tab>           # → "touch " (adds space)
touch <Tab>          # → "touch file1.txt" (first file)
touch <Tab><Tab>     # → "touch file2.py" (second file)
touch <Tab><Tab><Tab> # → "touch dir1/" (directory)
```

### 🏷️ **Aliases**
```bash
so    # → source
mk    # → mkdir  
his   # → history
```

### 📋 **Special Commands**
```bash
history     # Show last 200 commands
stats       # Usage statistics
clear       # Clear screen
exit/quit   # Exit
```

## 🆚 Comparison with Regular Terminal

| Feature | Regular Terminal | Smart Terminal |
|---------|-----------------|----------------|
| **Autosuggestion** | ❌ None | ✅ Real-time, intelligent |
| **Tab completion** | ⚡ Basic | 🚀 Multi-level, context-aware |
| **History** | 📝 Simple | 🧠 System integration + learning |
| **Command database** | ❌ None | ✅ 1000+ built-in commands |
| **Visual feedback** | 🔲 Monochrome | 🎨 Colorful, informative |
| **Git integration** | ❌ None | ✅ Branch display in prompt |
| **File completion** | ⚡ Basic | 🎯 Smart filtering by command |
| **Cross-session** | ⚡ Limited | ✅ Full sync with system |

## 🎯 Priority System

Smart Terminal uses a 6-level priority system:

1. **🏆 Priority 0: Aliases** (highest)
   - `so` → `source`
   - `mk` → `mkdir`

2. **⚡ Priority 1: Command Completion**
   - `touch` → `touch ` (adds space)
   - `gi` → `git`

3. **📁 Priority 2: File/Directory Completion**
   - `python ` → `python script.py`
   - `cd ` → `cd directory/`

4. **📚 Priority 3: Database Commands (Specific)**
   - `git ` → `git status`
   - `npm ` → `npm install`

5. **🔍 Priority 4: Database Commands (All)**
   - Search across entire database

6. **📜 Priority 5: History** (lowest)
   - Suggestions from command history

## 🛠️ Advanced Features

### 📊 **Statistics**
```bash
stats
```
Shows:
- Total commands used
- Top 10 most used commands
- Detailed statistics

### ⏱️ **Timing Mode**
```bash
python3 smart-terminal.py -t
```
- Shows execution time for each command
- Color-coded by speed:
  - 🟢 < 1s: Green
  - 🟡 1-60s: Yellow  
  - 🔴 > 60s: Red

### 🎨 **Custom Prompt**
```bash
username@hostname:directory (git:branch)$ 
```
- Shows user and hostname
- Current directory (directory name only)
- Git branch if in repository
- Beautiful colors

### 📂 **Smart File Completion**
- **Python commands**: Only shows `.py` files
- **Node commands**: Only shows `.js` files
- **C/C++ commands**: Shows `.c`, `.cpp`, `.h` files
- **Directory commands**: Only shows directories

## 🔧 Customization

### Adding New Aliases
Edit `smart-terminal.py`:
```python
self.aliases = {
    "so": "source",
    "mk": "mkdir", 
    "his": "history",
    "ll": "ls -la",        # Add new alias
    "la": "ls -A"          # Add new alias
}
```

### Adding New Commands
Add to `suggestions_db`:
```python
"your-command": [
    "your-command --help",
    "your-command --version",
    "your-command start",
]
```

## 🐛 Troubleshooting

### Common Issues

**1. ImportError or ModuleNotFoundError**
```bash
# Ensure Python 3.6+
python3 --version

# Run from correct directory
cd /path/to/smart-terminal
python3 smart-terminal.py
```

**2. Cannot load history**
```bash
# Check if history files exist
ls -la ~/.zsh_history ~/.bash_history

# Check read permissions
chmod 644 ~/.zsh_history
```

**3. Suggestions not working**
- Ensure running in real terminal (not IDE)
- Terminal must support ANSI colors
- Check if `.smart_terminal_db.json` is created

## 📈 Future Roadmap

- 🔍 **Fuzzy search**: Approximate string matching
- 🤖 **AI suggestions**: Use AI for smarter suggestions
- 🌐 **Plugin system**: Support for third-party plugins
- 📱 **Mobile support**: Support for Termux on Android
- 🔄 **Auto-update**: Automatic command database updates

## 📄 License

MIT License - Free to use for personal and commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

Inspired by:
- Oh My Zsh
- Fish shell autosuggestions
- PowerShell predictive IntelliSense

---

**Made with ❤️ for developers who love efficiency**
