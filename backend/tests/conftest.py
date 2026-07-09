import pytest
import subprocess
import time
import os
import signal
import socket


def _is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


@pytest.fixture(scope="module")
def server_url():
    # 如果已有服务占用了 8000 端口，先杀掉
    if _is_port_in_use(8000):
        subprocess.run(["pkill", "-f", "uvicorn main:app"], check=False)
        time.sleep(1)

    if os.path.exists("math_practice.db"):
        os.remove("math_practice.db")

    proc = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )
    time.sleep(3)

    yield "http://localhost:8000"

    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    proc.wait(timeout=5)
