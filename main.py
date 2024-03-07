import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.proc = None
        self.start_program()

    def start_program(self):
        print("Starting main.py...")
        self.proc = subprocess.Popen(["python", "main.py"])

    def restart_program(self):
        print("Restarting main.py...")
        self.proc.kill()  # Kill the current process
        self.start_program()

    def on_modified(self, event):
        print("File modified. Reloading...")
        self.restart_program()

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()