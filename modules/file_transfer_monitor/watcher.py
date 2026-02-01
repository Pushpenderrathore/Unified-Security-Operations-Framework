from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileTransferHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[!] File modified: {event.src_path}")

def start_monitor(path="/tmp"):
    observer = Observer()
    observer.schedule(FileTransferHandler(), path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
