# merged_runner.py
"""
Launcher that runs main.py (music bot) and mng2.py (management bot) as separate subprocesses.
This preserves their original behavior (no in-file modifications needed) and ensures both
run concurrently in one terminal session.

Place this file in the same directory as main.py and mng2.py and run:
    python merged_runner.py

It will:
 - Start both scripts using the same Python interpreter.
 - Restart a script if it crashes (simple auto-restart).
 - Terminate both on Ctrl+C gracefully.
"""

import subprocess
import sys
import os
import time
import signal

PY = sys.executable
BASE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(BASE, "main.py")
MNG = os.path.join(BASE, "mng.py")

if not os.path.exists(MAIN):
    print("ERROR: main.py not found in", BASE)
    sys.exit(1)
if not os.path.exists(MNG):
    print("ERROR: mng.py not found in", BASE)
    sys.exit(1)

procs = {}

def start(name, path):
    print(f"[launcher] Starting {name} -> {path}")
    env = os.environ.copy()
    # Keep PYTHONUNBUFFERED for real-time logs
    env.setdefault("PYTHONUNBUFFERED", "1")
    p = subprocess.Popen([PY, path], env=env)
    procs[name] = p
    return p

def stop_all():
    print("[launcher] Stopping all child processes...")
    for name, p in list(procs.items()):
        try:
            print(f"[launcher] Terminating {name} (pid={p.pid})")
            p.terminate()
        except Exception as e:
            print(f"[launcher] Error terminating {name}: {e}")
    # give them a few seconds
    time.sleep(2)
    for name, p in list(procs.items()):
        if p.poll() is None:
            try:
                print(f"[launcher] Killing {name} (pid={p.pid})")
                p.kill()
            except Exception as e:
                print(f"[launcher] Error killing {name}: {e}")

def handle_sigint(signum, frame):
    stop_all()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)
signal.signal(signal.SIGTERM, handle_sigint)

# Start both processes
start("main", MAIN)
time.sleep(1)
start("mng", MNG)

# monitor and restart if needed
try:
    while True:
        time.sleep(2)
        for name, p in list(procs.items()):
            if p.poll() is not None:
                print(f"[launcher] {name} exited with code {p.returncode}. Restarting in 2s.")
                time.sleep(2)
                start(name, MAIN if name == "main" else MNG)
except KeyboardInterrupt:
    stop_all()
    print("[launcher] Exiting.")
