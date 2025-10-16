# launch.py
import os, sys, subprocess, webbrowser

def main():
    # Path handling for EXE and script mode
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    app_path = os.path.join(base_path, "app.py")
    port = "8501"

    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.port", port, "--browser.gatherUsageStats", "false"
    ]

    subprocess.Popen(cmd)
    webbrowser.open(f"http://localhost:{port}")

if __name__ == "__main__":
    main()
