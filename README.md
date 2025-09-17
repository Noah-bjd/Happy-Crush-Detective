# 🎉 Happy Crash Detective 🕵️‍♂️

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/happy-crash-detective/pulls)

A friendly, joyful debugger that makes crash analysis fun and understandable! Instead of scary technical jargon, get human-readable explanations with emojis and helpful tips.

![Demo](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzhrYmhkb2l2NGFxZDQ4OWs1azU3ZXFpZ3R3dGllOHVydXF3dnJjcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SV5k9Ulnk9LdgYnjbe/giphy.gif)

## ✨ Features

- 🎯 **Human-readable crash reports** with emojis and simple explanations
- 🐛 **Helpful tips** for common programming errors
- ⏰ **Works with both short-lived and long-running processes**
- 🎨 **Beautiful console output** with colors and clear formatting
- 🔗 **Attach to running processes** or debug new ones

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/happy-crash-detective.git

# Navigate to the directory
cd happy-crash-detective

# Make the script executable
chmod +x happy_debugger.py

# Install GDB if you don't have it
sudo apt install gdb  # Ubuntu/Debian
brew install gdb      # macOS
```

## 🚀 Quick Start

### Interactive Mode (Recommended)
```bash
./happy_debugger.py
```

### Command Line Mode
```bash
# Debug a program
./happy_debugger.py ./your_program arg1 arg2 

# Debug a long-running program
./happy_debugger.py ./your_server --long [FT_IRC-EXAMPlE]

```


## 🎨 Sample Output

```
🔍 🛑 Segmentation fault (tried to access memory that doesn't belong to you)

🎯 The problem is likely here:
   📁 File: server/Server_helper.cpp
   📄 Line: 61
   🔧 Function: XXXX:XXXXX

📋 What happened (simplified):
   1. main (started here)
   2. XXXX:XXXXX
   3. XXXX:XXXXX
   →  XXXX:XXXXX (crashed here)

💡 Hint: Your code called a system function that caused the crash.
   The system was trying to: xxxxxx

✨ Quick tips:
   • Check for null pointers
   • Verify array bounds
   • Ensure memory is properly allocated
   • Validate function inputs
```

## 🛠 Requirements

- Python 3.6+
- GDB (GNU Debugger)
- Programs compiled with debug symbols (`-g` flag)

## 🤝 Contributing

We love contributions! Here's how to help:

1. Fork the repository
2. Create a feature branch: `git checkout -b cool-new-feature`
3. Commit your changes: `git commit -am 'Add cool new feature'`
4. Push to the branch: `git push origin cool-new-feature`
5. Submit a pull request

## 🐛 Found a Bug?

Oops! Sorry about that. Please help us fix it:

1. Check if there's already an issue for the bug
2. If not, [create a new issue](https://github.com/yourusername/happy-crash-detective/issues/new)
3. Include:
   - What you were doing
   - What you expected to happen
   - What actually happened
   - Steps to reproduce the issue

(still needs works tho :shipit: )
