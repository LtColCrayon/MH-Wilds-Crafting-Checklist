import os
import sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(base_path, 'MHWildsChecklist.py')

    print(f"Launching checklist engine from: {script_path}")

    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())