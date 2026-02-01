from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

EVENTS = []

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            EVENTS.append({"file": event.src_path, "action": "CREATED"})

    def on_modified(self, event):
        if not event.is_directory:
            EVENTS.append({"file": event.src_path, "action": "MODIFIED"})

def start(path):
    observer = Observer()
    observer.schedule(Handler(), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    return EVENTS

