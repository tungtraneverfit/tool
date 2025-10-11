#!/usr/bin/env python3
"""
Smart Terminal với Autosuggestions thời gian thực
Giống Oh My Zsh - gợi ý ngay khi gõ
"""

import os
import sys
import json
import subprocess
import signal
import time
from pathlib import Path

# ANSI colors
GRAY = '\033[90m'
GREEN = '\033[92m'
BLUE = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

class SmartTerminal:
    def __init__(self):
        self.history_file = Path.home() / ".smart_terminal_history"
        self.db_file = Path.home() / ".smart_terminal_db.json"
        self.command_history = []
        self.suggestions_db = {}
        
        # Load data
        self.load_history()
        self.load_db()
        
    def load_history(self):
        """Load command history"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.command_history = [line.strip() for line in f.readlines() if line.strip()]
    
    def save_history(self):
        """Save command history"""
        with open(self.history_file, 'w') as f:
            # Keep last 5000 commands
            for cmd in self.command_history[-5000:]:
                f.write(f"{cmd}\n")
    
    def load_db(self):
        """Load suggestions database"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                self.suggestions_db = json.load(f)
        else:
            self.suggestions_db = {
                # Git
                "git": [
                    "git status",
                    "git add .",
                    "git add -A",
                    "git add -p",
                    "git commit -m \"\"",
                    "git commit -am \"\"",
                    "git commit --amend",
                    "git commit --amend --no-edit",
                    "git push",
                    "git push origin main",
                    "git push origin master",
                    "git push -f",
                    "git push --force-with-lease",
                    "git push -u origin ",
                    "git pull",
                    "git pull origin main",
                    "git pull origin master",
                    "git pull --rebase",
                    "git fetch",
                    "git fetch --all",
                    "git fetch --prune",
                    "git checkout ",
                    "git checkout -b ",
                    "git checkout main",
                    "git checkout master",
                    "git checkout -",
                    "git branch",
                    "git branch -a",
                    "git branch -d ",
                    "git branch -D ",
                    "git branch -m ",
                    "git log --oneline -15",
                    "git log",
                    "git log --oneline",
                    "git log --graph --oneline --all",
                    "git log -p",
                    "git log --stat",
                    "git log --author=\"\"",
                    "git log --since=\"1 week ago\"",
                    "git log --grep=\"\"",
                    "git diff",
                    "git diff HEAD",
                    "git diff --cached",
                    "git diff --staged",
                    "git diff HEAD~1",
                    "git diff branch1..branch2",
                    "git show ",
                    "git show HEAD",
                    "git show HEAD~1",
                    "git stash",
                    "git stash save \"\"",
                    "git stash list",
                    "git stash pop",
                    "git stash apply",
                    "git stash drop",
                    "git stash clear",
                    "git clone ",
                    "git clone --depth 1 ",
                    "git remote -v",
                    "git remote add origin ",
                    "git remote set-url origin ",
                    "git merge ",
                    "git merge --no-ff ",
                    "git merge --squash ",
                    "git rebase ",
                    "git rebase -i HEAD~",
                    "git rebase --continue",
                    "git rebase --abort",
                    "git reset HEAD",
                    "git reset --soft HEAD~1",
                    "git reset --hard HEAD",
                    "git reset --hard HEAD~1",
                    "git reset --hard origin/main",
                    "git clean -fd",
                    "git clean -fdx",
                    "git cherry-pick ",
                    "git tag",
                    "git tag -a ",
                    "git tag -d ",
                    "git blame ",
                    "git reflog",
                    "git rm ",
                    "git rm --cached ",
                    "git mv "
                ],
                
                # C++ Compilation
                "g++": [
                    "g++ main.cpp -o main",
                    "g++ -std=c++17 main.cpp -o main",
                    "g++ -std=c++20 main.cpp -o main",
                    "g++ -Wall -Wextra main.cpp -o main",
                    "g++ -g main.cpp -o main",
                    "g++ -O2 main.cpp -o main",
                    "g++ -O3 main.cpp -o main",
                    "g++ *.cpp -o main"
                ],
                "gcc": [
                    "gcc main.c -o main",
                    "gcc -Wall -Wextra main.c -o main",
                    "gcc -g main.c -o main",
                    "gcc -O2 main.c -o main"
                ],
                "cmake": [
                    "cmake .",
                    "cmake -B build",
                    "cmake --build build",
                    "cmake --build build --config Release",
                    "cmake -DCMAKE_BUILD_TYPE=Debug ..",
                    "cmake -DCMAKE_BUILD_TYPE=Release .."
                ],
                "make": [
                    "make",
                    "make clean",
                    "make all",
                    "make install",
                    "make -j4",
                    "make -j8"
                ],
                
                # Python
                "python": [
                    "python main.py",
                    "python -m venv venv",
                    "python -m pip install ",
                    "python -m pip install -r requirements.txt",
                    "python -m pip list",
                    "python -m pytest",
                    "python -m unittest discover",
                    "python -m http.server",
                    "python -m http.server 8000",
                    "python manage.py runserver",
                    "python manage.py migrate",
                    "python manage.py makemigrations",
                    "python manage.py createsuperuser",
                    "python -c \"\"",
                    "python -i"
                ],
                "python3": [
                    "python3 main.py",
                    "python3 -m venv venv",
                    "python3 -m pip install ",
                    "python3 -m pip install -r requirements.txt",
                    "python3 -m http.server 8000"
                ],
                "pip": [
                    "pip install ",
                    "pip install -r requirements.txt",
                    "pip install --upgrade pip",
                    "pip list",
                    "pip list --outdated",
                    "pip freeze > requirements.txt",
                    "pip uninstall ",
                    "pip show "
                ],
                "pip3": [
                    "pip3 install ",
                    "pip3 install -r requirements.txt",
                    "pip3 list",
                    "pip3 freeze > requirements.txt"
                ],
                
                # Linux System
                "ls": [
                    "ls -la",
                    "ls -lh",
                    "ls -lt",
                    "ls -ltr",
                    "ls -lS",
                    "ls -R"
                ],
                "cd": [
                    "cd ..",
                    "cd ~",
                    "cd -",
                    "cd /",
                    "cd /home",
                    "cd /var/log"
                ],
                "cat": [
                    "cat ",
                    "cat /etc/os-release",
                    "cat /proc/cpuinfo",
                    "cat /proc/meminfo"
                ],
                "grep": [
                    "grep -r \"\" .",
                    "grep -rn \"\" .",
                    "grep -i \"\" ",
                    "grep -v \"\" ",
                    "grep -E \"\" "
                ],
                "find": [
                    "find . -name \"\"",
                    "find . -type f -name \"\"",
                    "find . -type d -name \"\"",
                    "find . -name \"*.cpp\"",
                    "find . -name \"*.py\"",
                    "find . -name \"*.h\"",
                    "find . -mtime -1"
                ],
                "chmod": [
                    "chmod +x ",
                    "chmod 755 ",
                    "chmod 644 ",
                    "chmod -R 755 "
                ],
                "chown": [
                    "chown user:group ",
                    "chown -R user:group "
                ],
                "tar": [
                    "tar -czf archive.tar.gz ",
                    "tar -xzf archive.tar.gz",
                    "tar -xzvf archive.tar.gz",
                    "tar -tzf archive.tar.gz"
                ],
                "ps": [
                    "ps aux",
                    "ps aux | grep ",
                    "ps -ef",
                    "ps -eLf"
                ],
                "kill": [
                    "kill -9 ",
                    "kill -15 ",
                    "killall "
                ],
                "top": [
                    "top",
                    "top -u ",
                    "htop"
                ],
                "df": [
                    "df -h",
                    "df -i",
                    "df -T"
                ],
                "du": [
                    "du -sh *",
                    "du -sh .",
                    "du -h --max-depth=1"
                ],
                "free": [
                    "free -h",
                    "free -m"
                ],
                "systemctl": [
                    "systemctl status ",
                    "systemctl start ",
                    "systemctl stop ",
                    "systemctl restart ",
                    "systemctl enable ",
                    "systemctl disable ",
                    "systemctl list-units"
                ],
                "journalctl": [
                    "journalctl -xe",
                    "journalctl -u ",
                    "journalctl -f",
                    "journalctl --since today"
                ],
                "tail": [
                    "tail -f ",
                    "tail -n 100 ",
                    "tail -f /var/log/syslog"
                ],
                "head": [
                    "head -n 20 ",
                    "head -n 100 "
                ],
                "wget": [
                    "wget ",
                    "wget -c ",
                    "wget -O "
                ],
                "curl": [
                    "curl ",
                    "curl -X GET ",
                    "curl -X POST ",
                    "curl -I ",
                    "curl -o file.txt "
                ],
                "ssh": [
                    "ssh user@host",
                    "ssh -i ~/.ssh/id_rsa user@host",
                    "ssh -p 22 user@host"
                ],
                "scp": [
                    "scp file user@host:/path",
                    "scp -r folder user@host:/path",
                    "scp user@host:/path/file ."
                ],
                "rsync": [
                    "rsync -avz source/ destination/",
                    "rsync -avz --progress source/ destination/",
                    "rsync -avz -e ssh source/ user@host:/path/"
                ],
                "vim": [
                    "vim ",
                    "vim ~/.bashrc",
                    "vim ~/.vimrc"
                ],
                "nano": [
                    "nano ",
                    "nano ~/.bashrc"
                ],
                
                # Docker
                "docker": [
                    "docker ps",
                    "docker ps -a",
                    "docker images",
                    "docker run -it ",
                    "docker exec -it ",
                    "docker logs -f ",
                    "docker stop ",
                    "docker rm ",
                    "docker rmi ",
                    "docker build -t ",
                    "docker pull ",
                    "docker push ",
                    "docker-compose up -d",
                    "docker-compose down",
                    "docker system prune -a"
                ],
                
                # GDB (Debugging C++)
                "gdb": [
                    "gdb ./program",
                    "gdb -q ./program",
                    "gdb --args ./program arg1 arg2"
                ],
                "valgrind": [
                    "valgrind ./program",
                    "valgrind --leak-check=full ./program",
                    "valgrind --tool=memcheck ./program"
                ],
                
                # Build tools
                "clang": [
                    "clang++ main.cpp -o main",
                    "clang++ -std=c++17 main.cpp -o main"
                ]
            }
            self.save_db()
    
    def save_db(self):
        """Save suggestions database"""
        with open(self.db_file, 'w') as f:
            json.dump(self.suggestions_db, f, indent=2)
    
    def get_suggestion(self, text):
        """Get suggestion for current text"""
        if not text:
            return ""
        
        # Priority 1: Search in recent history first (HIGHEST PRIORITY)
        # Look at last 100 commands for better relevance
        for cmd in reversed(self.command_history[-100:]):
            if cmd.startswith(text) and cmd != text:
                return cmd
        
        # Priority 2: Check if we can suggest a command name first
        # Example: "gi" -> "git"
        if ' ' not in text:
            for cmd_name in self.suggestions_db.keys():
                if cmd_name.startswith(text) and cmd_name != text:
                    return cmd_name
        
        # Priority 3: Search in database for full commands
        first_word = text.split()[0] if text.split() else text
        if first_word in self.suggestions_db:
            for cmd in self.suggestions_db[first_word]:
                if cmd.startswith(text) and cmd != text:
                    return cmd
        
        # Priority 4: Fallback - search all commands in database
        for cmd_list in self.suggestions_db.values():
            for cmd in cmd_list:
                if cmd.startswith(text) and cmd != text:
                    return cmd
        
        return ""
    
    def add_to_history(self, cmd):
        """Add command to history"""
        if cmd and cmd.strip():
            # Remove from history if exists (to move to end)
            if cmd in self.command_history:
                self.command_history.remove(cmd)
            
            # Add to end
            self.command_history.append(cmd)
            self.save_history()
    
    def get_prompt(self):
        """Get custom prompt"""
        cwd = os.getcwd()
        home = str(Path.home())
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
        
        return f"{BLUE}❯{RESET} "
    
    def run_command(self, cmd):
        """Execute shell command"""
        if not cmd.strip():
            return
        
        # Special commands
        if cmd in ['exit', 'quit']:
            print(f"{GREEN}👋 Tạm biệt!{RESET}")
            sys.exit(0)
        
        if cmd == 'clear':
            os.system('clear' if os.name != 'nt' else 'cls')
            return
        
        if cmd == 'history':
            print(f"\n{YELLOW}📜 Lịch sử lệnh (20 gần nhất):{RESET}")
            for i, h in enumerate(self.command_history[-20:], 1):
                print(f"  {i}. {h}")
            print()
            return
        
        if cmd == 'stats':
            self.show_stats()
            return
        
        # Execute command with timing
        try:
            start_time = time.time()
            result = subprocess.run(cmd, shell=True, executable='/bin/bash')
            end_time = time.time()
            
            # Calculate execution time
            elapsed = end_time - start_time
            
            # Show execution time with color coding
            if elapsed < 1:
                time_str = f"{elapsed*1000:.0f}ms"
                color = GREEN
            elif elapsed < 60:
                time_str = f"{elapsed:.2f}s"
                color = YELLOW
            else:
                minutes = int(elapsed // 60)
                seconds = elapsed % 60
                time_str = f"{minutes}m {seconds:.1f}s"
                color = RED
            
            # Show timing info
            print(f"{color}⏱  {time_str}{RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{YELLOW}^C{RESET}")
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
    
    def show_stats(self):
        """Show statistics"""
        print(f"\n{GREEN}╔════════════════════════════════════════╗{RESET}")
        print(f"{GREEN}║  Smart Terminal Statistics            ║{RESET}")
        print(f"{GREEN}╚════════════════════════════════════════╝{RESET}\n")
        
        print(f"{BLUE}📊 Thống kê:{RESET}")
        print(f"   Tổng số lệnh: {len(self.command_history)}")
        print()
        
        if self.command_history:
            print(f"{BLUE}🔥 Top 10 lệnh:{RESET}")
            from collections import Counter
            counter = Counter(self.command_history)
            for cmd, count in counter.most_common(10):
                print(f"   {GREEN}{count:3d}x{RESET}  {cmd}")
        print()
    
    def handle_input_with_suggestion(self):
        """Handle input with live suggestions using termios"""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(fd)
            
            current_input = ""
            
            # Print initial prompt
            prompt = self.get_prompt()
            sys.stdout.write(prompt)
            sys.stdout.flush()
            
            while True:
                # Read one character
                ch = sys.stdin.read(1)
                
                # Handle Enter
                if ch == '\r' or ch == '\n':
                    sys.stdout.write('\r\n')
                    sys.stdout.flush()
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    return current_input
                
                # Handle Backspace
                elif ch == '\x7f':
                    if current_input:
                        current_input = current_input[:-1]
                        # Redraw line
                        sys.stdout.write('\r\033[K')  # Clear line
                        sys.stdout.write(prompt + current_input)
                        
                        # Show suggestion
                        suggestion = self.get_suggestion(current_input)
                        if suggestion and len(suggestion) > len(current_input):
                            remaining = suggestion[len(current_input):]
                            sys.stdout.write(f"{GRAY}{remaining}{RESET}")
                            sys.stdout.write('\b' * len(remaining))
                        
                        sys.stdout.flush()
                
                # Handle Ctrl+C
                elif ch == '\x03':
                    sys.stdout.write('\r\n')
                    sys.stdout.flush()
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    raise KeyboardInterrupt
                
                # Handle Ctrl+D
                elif ch == '\x04':
                    if not current_input:
                        sys.stdout.write('\r\n')
                        sys.stdout.flush()
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        return 'exit'
                
                # Handle Escape sequences (arrow keys, etc)
                elif ch == '\x1b':
                    seq = sys.stdin.read(2)
                    
                    # Right arrow - accept suggestion
                    if seq == '[C':
                        suggestion = self.get_suggestion(current_input)
                        if suggestion:
                            # Clear old display
                            sys.stdout.write('\r\033[K')
                            current_input = suggestion
                            sys.stdout.write(prompt + current_input)
                            sys.stdout.flush()
                    
                    # Up arrow - previous command
                    elif seq == '[A':
                        if self.command_history:
                            sys.stdout.write('\r\033[K')
                            current_input = self.command_history[-1]
                            sys.stdout.write(prompt + current_input)
                            sys.stdout.flush()
                
                # Handle Tab - accept suggestion
                elif ch == '\t':
                    suggestion = self.get_suggestion(current_input)
                    if suggestion:
                        # Clear old display
                        sys.stdout.write('\r\033[K')
                        current_input = suggestion
                        sys.stdout.write(prompt + current_input)
                        sys.stdout.flush()
                
                # Handle printable characters
                elif ch >= ' ' and ch <= '~':
                    current_input += ch
                    
                    # Clear line and redraw
                    sys.stdout.write('\r\033[K')
                    sys.stdout.write(prompt + current_input)
                    
                    # Get and show suggestion
                    suggestion = self.get_suggestion(current_input)
                    if suggestion and len(suggestion) > len(current_input):
                        remaining = suggestion[len(current_input):]
                        sys.stdout.write(f"{GRAY}{remaining}{RESET}")
                        # Move cursor back
                        sys.stdout.write('\b' * len(remaining))
                    
                    sys.stdout.flush()
        
        except Exception as e:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            raise e
    
    def run(self):
        """Main loop"""
        # Welcome message
        print(f"{GREEN}╔════════════════════════════════════════╗{RESET}")
        print(f"{GREEN}║  ✨ Smart Terminal v2.0               ║{RESET}")
        print(f"{GREEN}║  Gợi ý dựa trên history của bạn       ║{RESET}")
        print(f"{GREEN}║  Nhấn Tab hoặc → để chấp nhận         ║{RESET}")
        print(f"{GREEN}╚════════════════════════════════════════╝{RESET}\n")
        
        print(f"{YELLOW}💡 Lệnh: stats, history, clear, exit{RESET}")
        print(f"{GRAY}💡 Càng dùng nhiều, gợi ý càng thông minh!{RESET}\n")
        
        try:
            while True:
                try:
                    # Get input with suggestions
                    cmd = self.handle_input_with_suggestion()
                    
                    if cmd and cmd.strip():
                        # Run command
                        self.run_command(cmd)
                        # Add to history
                        self.add_to_history(cmd)
                
                except KeyboardInterrupt:
                    print(f"{YELLOW}Nhấn Ctrl+D hoặc gõ 'exit' để thoát{RESET}")
                    continue
                
        except (EOFError, SystemExit):
            print(f"{GREEN}👋 Tạm biệt!{RESET}")

def main():
    # Handle signals
    def signal_handler(sig, frame):
        print(f"\n{GREEN}👋 Tạm biệt!{RESET}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if running in proper terminal
    if not sys.stdin.isatty():
        print("Error: Must run in an interactive terminal")
        sys.exit(1)
    
    # Run terminal
    terminal = SmartTerminal()
    terminal.run()

if __name__ == "__main__":
    main()
