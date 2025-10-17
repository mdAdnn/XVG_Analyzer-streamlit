import os
import sys
import subprocess
import threading
import time
import socket
import webbrowser

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def find_free_port(start=8501, end=8600):
    for port in range(start, end):
        if not is_port_in_use(port):
            return port
    raise RuntimeError("No free port available")

def run_streamlit(port):
    """Launch Streamlit as a subprocess."""
    env = os.environ.copy()
    env["STREAMLIT_SERVER_PORT"] = str(port)
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        os.path.join(os.path.dirname(__file__), "app.py"),
        "--server.port", str(port),
        "--server.headless", "true"
    ]
    return subprocess.Popen(cmd, env=env)

def main():
    # Prevent multiple instances of the EXE
    import psutil
    exe_name = os.path.basename(sys.argv[0])
    count = sum(1 for p in psutil.process_iter(['name']) if p.info['name'] == exe_name)
    if count > 1:
        print("Duplicate instance detected — exiting.")
        sys.exit(0)

    port = find_free_port()
    p = run_streamlit(port)

    # Wait a moment, then open browser
    time.sleep(2)
    webbrowser.open(f"http://localhost:{port}")

    # Keep process alive while Streamlit runs
    try:
        p.wait()
    except KeyboardInterrupt:
        p.terminate()

if __name__ == "__main__":
    main()
