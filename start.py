import subprocess
import sys
import signal
import time

processes = []


def start(cmd):
    p = subprocess.Popen(cmd, shell=True)
    processes.append(p)


def shutdown(signum, frame):
    print("\nShutting down processes...")
    for p in processes:
        p.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


if __name__ == "__main__":
    print("Starting bot and scheduler...")

    start("python -m app.bot")
    start("python -m app.scheduler")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)
