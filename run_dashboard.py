import os
import sys
import subprocess

if __name__ == "__main__":
    python_exe = sys.executable

    cmd = [python_exe, "-m", "streamlit", "run", "MHWildsChecklist.py"]

    print(f"Launching dashboard using: {python_exe}")
    
    subprocess.Popen(cmd)