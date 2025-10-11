#!/usr/bin/env python3
"""
Smart Terminal with Real-time Autosuggestions
Like Oh My Zsh - suggests as you type
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
    def __init__(self, show_timing=False):
        self.history_file = Path.home() / ".smart_terminal_history"
        self.db_file = Path.home() / ".smart_terminal_db.json"
        self.command_history = []
        self.suggestions_db = {}
        self.show_timing = show_timing  # Flag to control timing display
        
        # Command aliases (shortcuts) - defined here for immediate use
        self.aliases = {
            "so": "source",
            "mk": "mkdir",
            "his": "history"
        }
        
        # Load data
        self.load_history()
        self.load_db()
        
    def load_history(self):
        """Load command history"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.command_history = [line.strip() for line in f.readlines() if line.strip()]
        
        # Debug: Print history info on startup
        print(f"{GRAY}📚 Loaded {len(self.command_history)} commands from history{RESET}")
        if len(self.command_history) > 0:
            print(f"{GRAY}   Last command: {self.command_history[-1][:50]}{'...' if len(self.command_history[-1]) > 50 else ''}{RESET}")
    
    
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
                    "gcc -O2 main.c -o main",
                    "gcc -O3 main.c -o main",
                    "gcc -std=c99 main.c -o main",
                    "gcc -std=c11 main.c -o main",
                    "gcc -std=c17 main.c -o main",
                    "gcc -Wall -Wextra -Werror main.c -o main",
                    "gcc -pedantic main.c -o main",
                    "gcc -pthread main.c -o main",
                    "gcc -lm main.c -o main",
                    "gcc -shared -fPIC lib.c -o lib.so",
                    "gcc *.c -o main"
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
                    "make -j8",
                    "make -j$(nproc)",
                    "make test",
                    "make check",
                    "make distclean",
                    "make uninstall",
                    "make help",
                    "make debug",
                    "make release"
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
                
                # Node.js & JavaScript
                "node": [
                    "node ",
                    "node index.js",
                    "node app.js",
                    "node server.js",
                    "node -v",
                    "node --version",
                    "node -e \"\"",
                    "node --inspect ",
                    "node --watch "
                ],
                "npm": [
                    "npm init",
                    "npm init -y",
                    "npm install",
                    "npm install ",
                    "npm install --save ",
                    "npm install --save-dev ",
                    "npm install -g ",
                    "npm install react react-dom",
                    "npm install express",
                    "npm install axios",
                    "npm install dotenv",
                    "npm install cors",
                    "npm install nodemon --save-dev",
                    "npm install typescript --save-dev",
                    "npm install @types/node --save-dev",
                    "npm uninstall ",
                    "npm update",
                    "npm update ",
                    "npm outdated",
                    "npm list",
                    "npm list -g --depth=0",
                    "npm run ",
                    "npm run dev",
                    "npm run build",
                    "npm run start",
                    "npm run test",
                    "npm start",
                    "npm test",
                    "npm run lint",
                    "npm run format",
                    "npm cache clean --force",
                    "npm audit",
                    "npm audit fix",
                    "npm audit fix --force",
                    "npm ci",
                    "npm version patch",
                    "npm version minor",
                    "npm version major",
                    "npm publish",
                    "npm search ",
                    "npm info ",
                    "npm config list",
                    "npm config get registry",
                    "npm config set registry "
                ],
                "npx": [
                    "npx ",
                    "npx create-react-app ",
                    "npx create-next-app ",
                    "npx create-vite ",
                    "npx tsc --init",
                    "npx eslint --init",
                    "npx prettier --write .",
                    "npx json-server --watch db.json",
                    "npx serve",
                    "npx nodemon "
                ],
                "yarn": [
                    "yarn",
                    "yarn init",
                    "yarn init -y",
                    "yarn add ",
                    "yarn add --dev ",
                    "yarn add -D ",
                    "yarn global add ",
                    "yarn remove ",
                    "yarn upgrade",
                    "yarn upgrade ",
                    "yarn install",
                    "yarn run ",
                    "yarn dev",
                    "yarn build",
                    "yarn start",
                    "yarn test",
                    "yarn lint",
                    "yarn cache clean"
                ],
                "pnpm": [
                    "pnpm install",
                    "pnpm add ",
                    "pnpm add -D ",
                    "pnpm remove ",
                    "pnpm update",
                    "pnpm run ",
                    "pnpm dev",
                    "pnpm build",
                    "pnpm start",
                    "pnpm test"
                ],
                "nvm": [
                    "nvm install ",
                    "nvm install node",
                    "nvm install --lts",
                    "nvm use ",
                    "nvm use node",
                    "nvm use --lts",
                    "nvm list",
                    "nvm ls",
                    "nvm ls-remote",
                    "nvm current",
                    "nvm alias default ",
                    "nvm uninstall ",
                    "nvm which ",
                    "nvm --version"
                ],
                "nodemon": [
                    "nodemon ",
                    "nodemon index.js",
                    "nodemon server.js",
                    "nodemon --watch src"
                ],
                "tsx": [
                    "tsx ",
                    "tsx watch ",
                    "tsx index.ts"
                ],
                "tsc": [
                    "tsc",
                    "tsc --init",
                    "tsc --watch",
                    "tsc -w",
                    "tsc --noEmit",
                    "tsc --build"
                ],
                "eslint": [
                    "eslint .",
                    "eslint --init",
                    "eslint --fix .",
                    "eslint src/"
                ],
                "prettier": [
                    "prettier --write .",
                    "prettier --check .",
                    "prettier --write src/"
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
                
                # File operations
                "rm": [
                    "rm ",
                    "rm -i ",
                    "rm -f ",
                    "rm -r ",
                    "rm -rf ",
                    "rm -rf *",
                    "rm -rf ./",
                    "rm -rI ",
                    "rm -v "
                ],
                "mv": [
                    "mv ",
                    "mv -i ",
                    "mv -n ",
                    "mv -v "
                ],
                "cp": [
                    "cp ",
                    "cp -r ",
                    "cp -a ",
                    "cp -i ",
                    "cp -v ",
                    "cp -p "
                ],
                "mkdir": [
                    "mkdir ",
                    "mkdir -p ",
                    "mkdir -v "
                ],
                
                # Shell built-ins and utilities
                "history": [
                    "history",
                    "history | grep ",
                    "history | tail -n 20",
                    "history | head -n 20",
                    "history -c"
                ],
                "alias": [
                    "alias",
                    "alias ll='ls -la'",
                    "alias la='ls -A'",
                    "alias l='ls -CF'"
                ],
                "export": [
                    "export PATH=$PATH:",
                    "export ",
                    "export -p"
                ],
                "source": [
                    "source ~/.bashrc",
                    "source ~/.bash_profile",
                    "source "
                ],
                "echo": [
                    "echo ",
                    "echo $PATH",
                    "echo $HOME",
                    "echo \"\"",
                    "echo -e "
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
        
        # Priority 0: Check aliases first (HIGHEST)
        # Example: "so" -> "source", "mk" -> "mkdir"
        if text in self.aliases:
            return self.aliases[text]
        
        # Check if typing alias with arguments: "so " -> "source "
        for alias, full_cmd in self.aliases.items():
            if text.startswith(alias + " "):
                return full_cmd + text[len(alias):]
        
        # Priority 1: Command name completion and exact matches
        # Example: "gi" -> "git", "touch" -> "touch " (add space)
        if ' ' not in text:
            # First check for exact command matches - add space
            known_commands = ['touch', 'mkdir', 'rm', 'mv', 'cp', 'cat', 'vim', 'nano', 
                            'python', 'python3', 'node', 'gcc', 'g++', 'git', 'ls', 'cd',
                            'less', 'more', 'head', 'tail', 'chmod', 'chown', 'source', 
                            'bash', 'sh', 'echo', 'grep', 'find', 'tar', 'zip', 'unzip']
            
            db_commands = list(self.suggestions_db.keys())
            all_commands = list(set(known_commands + db_commands))
            
            # Check for exact match first
            if text in all_commands:
                return text + " "
            
            # Then check for partial matches from database
            matching_cmds = []
            for cmd_name in self.suggestions_db.keys():
                if cmd_name.startswith(text) and cmd_name != text:
                    matching_cmds.append(cmd_name)
            
            # Sort by length to prefer shorter matches first
            if matching_cmds:
                matching_cmds.sort(key=len)
                return matching_cmds[0]
        
        # Priority 2: File/Directory completion for certain commands
        # If command ends with space, suggest files or directories
        if ' ' in text:
            parts = text.split()
            cmd_name = parts[0]
            
            # Commands that should autocomplete with files
            file_commands = ['python', 'python3', 'node', 'gcc', 'g++', 'cat', 'vim', 
                           'nano', 'less', 'more', 'head', 'tail', 'rm', 'mv', 'cp',
                           'chmod', 'chown', 'source', 'bash', 'sh', 'touch']
            
            # Commands that should autocomplete with directories only
            dir_commands = ['cd', 'mkdir', 'rmdir']
            
            # All commands that support path completion
            all_path_commands = file_commands + dir_commands
            
            # Handle path completion (works for both files and directories)
            if cmd_name in all_path_commands:
                # Get the last argument (path being typed)
                if len(parts) > 1:
                    current_path = parts[-1]
                else:
                    current_path = ""
                
                # Check if we're completing after a slash
                if '/' in current_path:
                    # Split path into directory and partial name
                    path_parts = current_path.rsplit('/', 1)
                    base_dir = path_parts[0]
                    partial = path_parts[1] if len(path_parts) > 1 else ""
                    
                    # Determine the directory to search in
                    if base_dir.startswith('/'):
                        search_dir = base_dir
                    elif base_dir.startswith('~'):
                        search_dir = os.path.expanduser(base_dir)
                    else:
                        search_dir = os.path.join(os.getcwd(), base_dir)
                    
                    try:
                        if os.path.isdir(search_dir):
                            items = []
                            
                            # For directory-only commands, only show directories
                            if cmd_name in dir_commands:
                                items = [d for d in os.listdir(search_dir)
                                       if os.path.isdir(os.path.join(search_dir, d))
                                       and d.startswith(partial)
                                       and not d.startswith('.')]
                            
                            # For file commands, show files first, then directories
                            else:
                                files = []
                                dirs = []
                                
                                # Get file extension filter based on command
                                if cmd_name in ['python', 'python3']:
                                    files = [f for f in os.listdir(search_dir)
                                            if os.path.isfile(os.path.join(search_dir, f))
                                            and f.endswith('.py')
                                            and f.startswith(partial)
                                            and not f.startswith('.')]
                                elif cmd_name == 'node':
                                    files = [f for f in os.listdir(search_dir)
                                            if os.path.isfile(os.path.join(search_dir, f))
                                            and f.endswith('.js')
                                            and f.startswith(partial)
                                            and not f.startswith('.')]
                                elif cmd_name in ['gcc', 'g++']:
                                    files = [f for f in os.listdir(search_dir)
                                            if os.path.isfile(os.path.join(search_dir, f))
                                            and f.endswith(('.c', '.cpp', '.cc', '.h', '.hpp'))
                                            and f.startswith(partial)
                                            and not f.startswith('.')]
                                else:
                                    files = [f for f in os.listdir(search_dir)
                                            if os.path.isfile(os.path.join(search_dir, f))
                                            and f.startswith(partial)
                                            and not f.startswith('.')]
                                
                                # Also get directories as fallback
                                dirs = [d for d in os.listdir(search_dir)
                                       if os.path.isdir(os.path.join(search_dir, d))
                                       and d.startswith(partial)
                                       and not d.startswith('.')]
                                
                                # Prioritize files, fallback to directories
                                items = files if files else dirs
                            
                            if items:
                                items.sort()
                                # Reconstruct the full path
                                new_path = base_dir + '/' + items[0]
                                return ' '.join(parts[:-1]) + (' ' if len(parts) > 1 else '') + new_path
                    except:
                        pass
                
                # No slash - complete from current directory
                elif text.endswith(' '):
                    try:
                        current_dir = os.getcwd()
                        items = []
                        
                        # For directory commands
                        if cmd_name in dir_commands:
                            items = [d for d in os.listdir(current_dir) 
                                   if os.path.isdir(os.path.join(current_dir, d)) 
                                   and not d.startswith('.')]
                        
                        # For file commands
                        else:
                            files = []
                            
                            if cmd_name in ['python', 'python3']:
                                files = [f for f in os.listdir(current_dir) if f.endswith('.py')]
                            elif cmd_name == 'node':
                                files = [f for f in os.listdir(current_dir) if f.endswith('.js')]
                            elif cmd_name in ['gcc', 'g++']:
                                files = [f for f in os.listdir(current_dir) 
                                        if f.endswith(('.c', '.cpp', '.cc', '.h', '.hpp'))]
                            else:
                                files = os.listdir(current_dir)
                            
                            # Filter out hidden files
                            files = [f for f in files if not f.startswith('.')]
                            
                            # Get directories as fallback
                            dirs = [d for d in os.listdir(current_dir) 
                                   if os.path.isdir(os.path.join(current_dir, d)) 
                                   and not d.startswith('.')]
                            
                            # Prioritize files, fallback to directories
                            items = files if files else dirs
                        
                        if items:
                            items.sort()
                            return text + items[0]
                    except:
                        pass
                
                # Typing partial name (no slash yet)
                elif len(parts) > 1 and current_path and '/' not in current_path:
                    try:
                        current_dir = os.getcwd()
                        items = []
                        
                        # For directory commands
                        if cmd_name in dir_commands:
                            items = [d for d in os.listdir(current_dir) 
                                   if os.path.isdir(os.path.join(current_dir, d)) 
                                   and d.startswith(current_path) 
                                   and not d.startswith('.')]
                        
                        # For file commands
                        else:
                            files = []
                            
                            if cmd_name in ['python', 'python3']:
                                files = [f for f in os.listdir(current_dir) 
                                        if f.endswith('.py') and f.startswith(current_path)]
                            elif cmd_name == 'node':
                                files = [f for f in os.listdir(current_dir) 
                                        if f.endswith('.js') and f.startswith(current_path)]
                            elif cmd_name in ['gcc', 'g++']:
                                files = [f for f in os.listdir(current_dir) 
                                        if f.endswith(('.c', '.cpp', '.cc', '.h', '.hpp')) 
                                        and f.startswith(current_path)]
                            else:
                                files = [f for f in os.listdir(current_dir) if f.startswith(current_path)]
                            
                            # Filter out hidden files
                            files = [f for f in files if not f.startswith('.')]
                            
                            # Get directories as fallback
                            dirs = [d for d in os.listdir(current_dir) 
                                   if os.path.isdir(os.path.join(current_dir, d)) 
                                   and d.startswith(current_path) 
                                   and not d.startswith('.')]
                            
                            # Prioritize files, fallback to directories
                            items = files if files else dirs
                        
                        if items:
                            items.sort()
                            return ' '.join(parts[:-1]) + ' ' + items[0]
                    except:
                        pass
            

        
        # Priority 3: Search in database for full commands
        # Only when user has typed the complete command name + space or more
        first_word = text.split()[0] if text.split() else text
        if first_word in self.suggestions_db:
            for cmd in self.suggestions_db[first_word]:
                if cmd.startswith(text) and cmd != text:
                    return cmd
        
        # Priority 4: Fallback - search all commands in database
        for cmd_list in self.suggestions_db.values():
            if isinstance(cmd_list, list):
                for cmd in cmd_list:
                    if cmd.startswith(text) and cmd != text:
                        return cmd
        
        # Priority 5: Search in recent history (LOWEST PRIORITY)
        # Look at last 100 commands for better relevance
        for cmd in reversed(self.command_history[-100:]):
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
    
    def get_git_branch(self):
        """Get current git branch if in a git repository"""
        try:
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  text=True)
            branch = result.stdout.strip() if result.returncode == 0 else None
            return branch
        except Exception as e:
            return None
    
    def get_git_status(self):
        """Get git status info for prompt styling"""
        try:
            # Check if there are staged changes
            result_staged = subprocess.run(['git', 'diff', '--cached', '--quiet'], 
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            has_staged = result_staged.returncode != 0
            
            # Check if there are unstaged changes
            result_unstaged = subprocess.run(['git', 'diff', '--quiet'], 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            has_unstaged = result_unstaged.returncode != 0
            
            # Check if there are untracked files
            result_untracked = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], 
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            has_untracked = bool(result_untracked.stdout.strip())
            
            return {
                'staged': has_staged,
                'unstaged': has_unstaged,
                'untracked': has_untracked,
                'clean': not (has_staged or has_unstaged or has_untracked)
            }
        except:
            return {'staged': False, 'unstaged': False, 'untracked': False, 'clean': True}

    def get_prompt(self):
        """Get custom prompt like a real terminal"""
        cwd = os.getcwd()
        
        # Get just the current directory name
        if cwd == str(Path.home()):
            display_path = "~"
        else:
            display_path = os.path.basename(cwd)
        
        # Get user info
        username = os.getenv('USER', 'user')
        
        # Get git branch if available
        git_branch = self.get_git_branch()
        
        if git_branch:
            # Get git status for styling
            git_status = self.get_git_status()
            
            # Choose color based on git status
            if git_status['clean']:
                branch_color = GREEN  # Clean - green
            elif git_status['staged']:
                branch_color = YELLOW  # Staged changes - yellow
            else:
                branch_color = RED     # Unstaged/untracked - red
            
            # Compact format with bold: (user)directory git:(branch)$
            return f"{BOLD}({GREEN}{username}{RESET}{BOLD}){BLUE}{display_path}{RESET} {GRAY}git:({branch_color}{git_branch}{GRAY}){RESET}$ "
        else:
            # Compact format without git, with bold: (user)directory$
            return f"{BOLD}({GREEN}{username}{RESET}{BOLD}){BLUE}{display_path}{RESET}$ "
    
    def run_command(self, cmd):
        """Execute shell command"""
        if not cmd.strip():
            return
        
        # Special commands
        if cmd in ['exit', 'quit']:
            print(f"{GREEN}👋 Goodbye!{RESET}")
            sys.exit(0)
        
        if cmd == 'clear':
            os.system('clear' if os.name != 'nt' else 'cls')
            return
        
        if cmd == 'history':
            print(f"\n{YELLOW}📜 Command History (last 200):{RESET}")
            for i, h in enumerate(self.command_history[-200:], 1):
                print(f"  {i}. {h}")
            print()
            return
        
        if cmd == 'stats':
            self.show_stats()
            return
        
        # Special handling for cd command
        if cmd.startswith('cd ') or cmd == 'cd':
            try:
                # Parse the cd command
                parts = cmd.split(maxsplit=1)
                if len(parts) == 1:
                    # Just 'cd' - go to home directory
                    target_dir = os.path.expanduser('~')
                else:
                    target_dir = parts[1]
                    
                    # Handle special cases
                    if target_dir == '~':
                        target_dir = os.path.expanduser('~')
                    elif target_dir == '-':
                        # cd - (go to previous directory) - for now just go to home
                        target_dir = os.path.expanduser('~')
                    elif target_dir == '..':
                        target_dir = os.path.dirname(os.getcwd())
                    elif not target_dir.startswith('/'):
                        # Relative path
                        target_dir = os.path.join(os.getcwd(), target_dir)
                
                # Change directory
                old_dir = os.getcwd()
                os.chdir(target_dir)
                new_dir = os.getcwd()
                
                # Show change only if different from old directory
                if old_dir != new_dir:
                    # Show in a compact format like real terminals
                    pass  # Don't print anything, just like real terminals
                
            except FileNotFoundError:
                print(f"{RED}cd: no such file or directory: {parts[1] if len(parts) > 1 else '~'}{RESET}")
            except PermissionError:
                print(f"{RED}cd: permission denied: {parts[1] if len(parts) > 1 else '~'}{RESET}")
            except Exception as e:
                print(f"{RED}cd: {str(e)}{RESET}")
            return
        
        # Execute command with timing
        try:
            start_time = time.time()
            result = subprocess.run(cmd, shell=True, executable='/bin/bash')
            end_time = time.time()
            
            # Only show timing if flag is enabled
            if self.show_timing:
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
        
        print(f"{BLUE}📊 Statistics:{RESET}")
        print(f"   Total commands: {len(self.command_history)}")
        print()
        
        if self.command_history:
            print(f"{BLUE}🔥 Top 10 commands:{RESET}")
            from collections import Counter
            counter = Counter(self.command_history)
            for cmd, count in counter.most_common(10):
                print(f"   {GREEN}{count:3d}x{RESET}  {cmd}")
        print()
    
    def get_terminal_width(self):
        """Get terminal width, fallback to 80 if cannot determine"""
        try:
            import shutil
            return shutil.get_terminal_size().columns
        except:
            return 80
    
    def strip_ansi_codes(self, text):
        """Remove ANSI color codes from text for length calculation"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def safe_write_line(self, prompt, text):
        """Safely write a line, handling text that might be longer than terminal width"""
        terminal_width = self.get_terminal_width()
        prompt_len = len(self.strip_ansi_codes(prompt))
        available_width = terminal_width - prompt_len - 1  # -1 for safety margin
        
        # Clear the entire line first
        sys.stdout.write('\r\033[K')
        
        if len(text) <= available_width:
            # Text fits in one line
            sys.stdout.write(prompt + text)
        else:
            # Text is too long, truncate with ellipsis
            truncated = text[:available_width-3] + "..."
            sys.stdout.write(prompt + truncated)
        
        sys.stdout.flush()

    def handle_input_with_suggestion(self):
        """Handle input with live suggestions using termios"""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(fd)
            
            current_input = ""
            history_index = len(self.command_history)  # Start at end of history
            original_input = ""  # Store original input when browsing history
            
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
                        # Reset history index when user edits
                        history_index = len(self.command_history)
                        original_input = ""
                        
                        current_input = current_input[:-1]
                        # Redraw line safely
                        self.safe_write_line(prompt, current_input)
                        
                        # Show suggestion
                        suggestion = self.get_suggestion(current_input)
                        if suggestion and len(suggestion) > len(current_input):
                            remaining = suggestion[len(current_input):]
                            # Check if we have space for suggestion
                            terminal_width = self.get_terminal_width()
                            prompt_len = len(self.strip_ansi_codes(prompt))
                            if len(current_input) + len(remaining) + prompt_len < terminal_width - 1:
                                sys.stdout.write(f"{GRAY}{remaining}{RESET}")
                                sys.stdout.write('\b' * len(remaining))
                        
                        sys.stdout.flush()
                
                # Handle Ctrl+C
                elif ch == '\x03':
                    # Clear the line and move to new line
                    sys.stdout.write('\r\033[K^C\r\n')
                    sys.stdout.flush()
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    return None  # Return None to indicate cancelled command
                
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
                            current_input = suggestion
                            self.safe_write_line(prompt, current_input)
                    
                    # Up arrow - previous command in history
                    elif seq == '[A':
                        if self.command_history and history_index > 0:
                            # Save current input if we're at the end of history
                            if history_index == len(self.command_history):
                                original_input = current_input
                            
                            history_index -= 1
                            current_input = self.command_history[history_index]
                            
                            # Use safe write to handle long commands
                            self.safe_write_line(prompt, current_input)
                        else:
                            # If no history or at beginning, do nothing (or beep)
                            sys.stdout.write('\a')  # Bell sound
                            sys.stdout.flush()
                    
                    # Down arrow - next command in history
                    elif seq == '[B':
                        if self.command_history and history_index < len(self.command_history):
                            history_index += 1
                            
                            if history_index == len(self.command_history):
                                # Return to original input
                                current_input = original_input
                            else:
                                current_input = self.command_history[history_index]
                            
                            self.safe_write_line(prompt, current_input)
                            
                            # Show suggestion for current input
                            if history_index == len(self.command_history):
                                suggestion = self.get_suggestion(current_input)
                                if suggestion and len(suggestion) > len(current_input):
                                    remaining = suggestion[len(current_input):]
                                    # Check if we have space for suggestion
                                    terminal_width = self.get_terminal_width()
                                    prompt_len = len(self.strip_ansi_codes(prompt))
                                    if len(current_input) + len(remaining) + prompt_len < terminal_width - 1:
                                        sys.stdout.write(f"{GRAY}{remaining}{RESET}")
                                        sys.stdout.write('\b' * len(remaining))
                                    sys.stdout.flush()
                        else:
                            # If at end or no history, do nothing (or beep)
                            sys.stdout.write('\a')  # Bell sound
                            sys.stdout.flush()
                
                # Handle Tab - accept suggestion
                elif ch == '\t':
                    suggestion = self.get_suggestion(current_input)
                    if suggestion:
                        # Clear old display
                        current_input = suggestion
                        self.safe_write_line(prompt, current_input)
                
                # Handle printable characters
                elif ch >= ' ' and ch <= '~':
                    # Reset history index when user starts typing
                    history_index = len(self.command_history)
                    original_input = ""
                    
                    current_input += ch
                    
                    # Clear line and redraw safely
                    self.safe_write_line(prompt, current_input)
                    
                    # Get and show suggestion if there's space
                    suggestion = self.get_suggestion(current_input)
                    if suggestion and len(suggestion) > len(current_input):
                        remaining = suggestion[len(current_input):]
                        # Check if we have space for suggestion
                        terminal_width = self.get_terminal_width()
                        prompt_len = len(self.strip_ansi_codes(prompt))
                        if len(current_input) + len(remaining) + prompt_len < terminal_width - 1:
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
        print(f"{GREEN}║  Suggestions based on your history    ║{RESET}")
        print(f"{GREEN}║  Press Tab or → to accept             ║{RESET}")
        if self.show_timing:
            print(f"{GREEN}║  Timing mode: ENABLED                 ║{RESET}")
        print(f"{GREEN}╚════════════════════════════════════════╝{RESET}\n")
        
        print(f"{YELLOW}💡 Commands: stats, history, clear, exit{RESET}")
        print(f"{GRAY}💡 The more you use it, the smarter it gets!{RESET}")
        print(f"{GRAY}💡 Use ↑↓ arrows to browse command history{RESET}\n")
        
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
                    # Ctrl+C pressed - just continue to next prompt
                    continue
                
        except (EOFError, SystemExit):
            print(f"{GREEN}👋 Goodbye!{RESET}")

def main():
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Smart Terminal with autosuggestions')
    parser.add_argument('-t', '--timing', action='store_true', 
                        help='Enable timing mode - show execution time after each command')
    args = parser.parse_args()
    
    # Handle signals
    def signal_handler(sig, frame):
        print(f"\n{GREEN}👋 Goodbye!{RESET}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if running in proper terminal
    if not sys.stdin.isatty():
        print("Error: Must run in an interactive terminal")
        sys.exit(1)
    
    # Run terminal with timing mode if specified
    terminal = SmartTerminal(show_timing=args.timing)
    terminal.run()

if __name__ == "__main__":
    main()
