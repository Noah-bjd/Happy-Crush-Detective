#!/usr/bin/env python3
"""
🎉 Happy Crash Detective! 🕵️‍♂️
A friendly debugger that makes crash analysis fun and understandable!
"""

import sys
import subprocess
import re
import os
from typing import Optional, List, Tuple, Dict, Any

FRIENDLY_SIGNALS = {
    "SIGSEGV": "🛑 Segmentation fault (tried to access memory that doesn't belong to you)",
    "SIGABRT": "💥 Abort signal (program decided to quit unexpectedly)",
    "SIGFPE": "➗ Math error (division by zero or floating point issue)",
    "SIGILL": "⚡ Illegal instruction (CPU didn't understand your code)",
    "SIGBUS": "🚌 Bus error (misaligned memory access)",
    "SIGTRAP": "🔍 Trace/breakpoint trap (debugger is watching)",
    "SIGSYS": "📞 Bad system call (wrong number to the system)",
}

class HappyCrashDetective:
    def __init__(self):
        self.process = None
        self.attached_pid = None
        self.is_long_running = False
        self.monitoring_active = False
    
    def run_gdb(self, cmd: List[str], timeout: Optional[int] = None) -> str:
        """Run GDB with the specified command and return its output."""
        gdb_cmd = [
            "gdb", "--quiet", "--nx",
            "-ex", "set pagination off",
            "-ex", "set confirm off",
            "-ex", "handle SIGSEGV stop print nopass",
            "-ex", "handle SIGABRT stop print nopass",
            "-ex", "handle SIGFPE stop print nopass",
            "-ex", "handle SIGILL stop print nopass",
            "-ex", "handle SIGBUS stop print nopass",
            "-ex", "run",
            "-ex", "bt full",
            "-ex", "quit",
            "--args"
        ] + cmd

        try:
            result = subprocess.run(
                gdb_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                input="y\n"
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return "⏰ Time's up! Program took too long and was stopped."
        except FileNotFoundError:
            return "❌ Oops! GDB is not installed. Please install it with: sudo apt install gdb"
        except Exception as e:
            return f"❌ Whoops! Failed to run GDB: {str(e)}"
    
    def attach_gdb(self, pid: int) -> str:
        """Attach GDB to a running process and return its output."""
        gdb_cmd = [
            "gdb", "--quiet", "--nx",
            "-ex", "set pagination off",
            "-ex", "set confirm off",
            "-ex", "handle SIGSEGV stop print nopass",
            "-ex", "handle SIGABRT stop print nopass",
            "-ex", "handle SIGFPE stop print nopass",
            "-ex", "handle SIGILL stop print nopass",
            "-ex", "handle SIGBUS stop print nopass",
            "-ex", f"attach {pid}",
            "-ex", "continue",
            "-ex", "bt full",
            "-ex", "quit"
        ]

        try:
            result = subprocess.run(
                gdb_cmd,
                capture_output=True,
                text=True,
                input="y\n"
            )
            return result.stdout + result.stderr
        except FileNotFoundError:
            return "❌ Oops! GDB is not installed. Please install it with: sudo apt install gdb"
        except Exception as e:
            return f"❌ Whoops! Failed to attach GDB: {str(e)}"
    
    def parse_gdb_output(self, output: str) -> str:
        """Parse GDB output with friendly, understandable messages."""
        if not output:
            return "🤔 Hmm, no output to analyze. That's strange!"
        
        signal_detected = None
        for sig, desc in FRIENDLY_SIGNALS.items():
            if sig in output:
                signal_detected = sig
                break
        
        if not signal_detected:
            if "exited with code" in output:
                exit_code = re.search(r'exited with code (\d+)', output)
                if exit_code:
                    code = int(exit_code.group(1))
                    if code == 0:
                        return "🎉 Success! Program finished perfectly with code 0!"
                    else:
                        return f"⚠️  Program exited with error code {code} (not a crash, but something went wrong)"
            return "✅ No crash detected! Program finished normally."
        
        frame_pattern = r'#(\d+)\s+(0x[0-9a-fA-F]+)?\s+in\s+([^(]+)(\([^)]*\))?\s+\((?:[^)]*)\)\s+at\s+(.+?):(\d+)'
        frames = re.findall(frame_pattern, output)
        
        user_frames = []
        library_frames = []
        
        for frame in frames:
            frame_num, addr, func, params, file, line = frame
            full_func = func.strip() + (params if params else '')
            
            is_library = any([
                file.startswith('/usr'), file.startswith('/lib'),
                'sysdeps' in file, 'malloc' in file, '.so' in file,
                'libc' in file, 'libstdc++' in file, 'libpthread' in file,
                'ld-linux' in file, 'csu' in file, 'vg_preload' in file,
                'linux-gnu' in file, func.startswith('__GI_'),
                func.startswith('__libc_'), func.startswith('std::'),
                func.startswith('operator'),
            ])
            
            if is_library:
                library_frames.append((frame_num, full_func, file, line))
            else:
                user_frames.append((frame_num, full_func, file, line))
        
        result = f"\n🔍 {FRIENDLY_SIGNALS.get(signal_detected, 'Unknown error happened!')}\n\n"
        
        if user_frames:
            frame_num, func, file, line = user_frames[0]
            result += f"🎯 **The problem is likely here:**\n"
            result += f"   📁 File: {file}\n"
            result += f"   📄 Line: {line}\n"
            result += f"   🔧 Function: {func}\n\n"
            
            result += "📋 **What happened (simplified):**\n"
            if len(user_frames) > 1:
                result += f"   1. {user_frames[-1][1]} (started here)\n"
                for i in range(min(3, len(user_frames)-1)):
                    result += f"   {i+2}. {user_frames[-(i+2)][1]}\n"
                result += f"   → {user_frames[0][1]} (crashed here)\n"
            
            if library_frames:
                result += f"\n💡 **Hint:** Your code called a system function that caused the crash.\n"
                result += f"   The system was trying to: {library_frames[0][1]}\n"
                
        elif library_frames:
            result += "🤔 **The crash happened in a system library**\n"
            result += "💡 **This usually means:**\n"
            result += "   • You passed invalid data to a system function\n"
            result += "   • Memory was corrupted before the system call\n"
            result += "   • You're using a library function incorrectly\n\n"
            
            for frame_num, func, file, line in library_frames:
                if not any(lib_term in func for lib_term in ['std::', '__GI_', '__libc_']):
                    result += f"🔍 **Look at this code:** {func} at {file}:{line}\n"
                    break
        else:
            result += "🤷 **Couldn't find detailed crash information**\n"
            result += "💡 **Try this:** Compile with -g flag: g++ -g your_code.cpp\n"
        
        result += "\n✨ **Quick tips:**\n"
        result += "   • Check for null pointers\n"
        result += "   • Verify array bounds\n"
        result += "   • Ensure memory is properly allocated\n"
        result += "   • Validate function inputs\n"
        result += "   • Avoid double frees or invalid frees\n"
        result += "   • Use tools like Valgrind for memory issues\n"
        result += "   • Don't hesitate to ask for help! 🆘\n"
        
        return result

    def interactive_debug(self):
        """Interactive mode with friendly prompts."""
        print("\n" + "="*50)
        print("🎉 Welcome to Happy Crash Detective! 🕵️‍♂️")
        print("="*50)
        print("I'll help you find those pesky bugs! 🐛\n")
        
        while True:
            choice = input("Choose an option:\n"
                         "1️⃣  Debug a program\n"
                         "2️⃣  Attach to running program\n"
                         "3️⃣  Exit\n"
                         "👉 Your choice (1/2/3): ").strip()
            
            if choice == "1":
                self.debug_binary()
                break
            elif choice == "2":
                self.attach_process()
                break
            elif choice == "3":
                print("👋 Goodbye! Happy coding! 💻")
                sys.exit(0)
            else:
                print("❌ Please enter 1, 2, or 3")
    
    def debug_binary(self):
        """Debug a binary with friendly prompts."""
        while True:
            binary_path = input("\n📂 Enter path to your program: ").strip()
            if not binary_path:
                print("❌ Please provide a path")
                continue
            
            if not os.path.exists(binary_path):
                print(f"❌ File '{binary_path}' doesn't exist")
                continue
            
            if not os.access(binary_path, os.X_OK):
                print(f"❌ File '{binary_path}' isn't executable")
                continue
            
            break
        
        args_input = input("🔧 Enter arguments (press Enter for none): ").strip()
        args = args_input.split() if args_input else []
        
        self.is_long_running = input("⏰ Is this a long-running program? (y/N): ").strip().lower() == 'y'
        
        if self.is_long_running:
            cmd = [binary_path] + args
            self.monitor_long_running_process(cmd)
        else:
            timeout = 30
            cmd = [binary_path] + args
            print(f"\n🚀 Running: {' '.join(cmd)}")
            print("⏳ This might take a moment...")
            
            output = self.run_gdb(cmd, timeout)
            print("\n" + "="*50)
            print(self.parse_gdb_output(output))
            print("="*50)

    def attach_process(self):
        """Attach to a process with friendly prompts."""
        while True:
            try:
                pid_input = input("\n🔗 Enter PID of the process: ").strip()
                if not pid_input:
                    print("❌ Please provide a PID")
                    continue
                
                pid = int(pid_input)
                
                try:
                    os.kill(pid, 0)
                except OSError:
                    print(f"❌ Process {pid} doesn't exist or no permission")
                    continue
                
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        print(f"\n🔗 Attaching to process {pid}...")
        output = self.attach_gdb(pid)
        print("\n" + "="*50)
        print(self.parse_gdb_output(output))
        print("="*50)

def main():
    """Main function with happy startup message."""
    print("🎉 Starting Happy Crash Detective! 🕵️‍♂️")
    
    if len(sys.argv) > 1:
        debugger = HappyCrashDetective()
        cmd = sys.argv[1:]
        if sys.argv[1].isdigit():
            print("❌ First argument should be a binary or PID, not a number. [The PID feature will be added soon!]")
            return
        else:
            is_long_running = "--long" in cmd
            if is_long_running:
                cmd.remove("--long")
                debugger.monitor_long_running_process(cmd)
            else:
                timeout = 30
                output = debugger.run_gdb(cmd, timeout)
                print(debugger.parse_gdb_output(output))
    else:
        #debugger = HappyCrashDetective()
        #debugger.interactive_debug()
        print("❌ Please provide a binary to debug.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 interrupted. Goodbye! 😊")
        sys.exit(0)