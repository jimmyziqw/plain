import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileEventWriter(FileSystemEventHandler):
    def __init__(self, queue_file):
        self.queue_file = queue_file

    def log_event(self, path, status):
        event = {'path': path, 'status': status, 'timestamp': time.time()}
        with open(self.queue_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def on_modified(self, event):
        if not event.is_directory:
            print(f'File modified: {event.src_path}')
            self.log_event(event.src_path, 'modified')

    def on_created(self, event):
        if not event.is_directory:
            print(f'File created: {event.src_path}')
            self.log_event(event.src_path, 'created')

    def on_deleted(self, event):
        if not event.is_directory:
            print(f'File deleted: {event.src_path}')
            self.log_event(event.src_path, 'deleted')

if __name__ == "__main__":
    path_to_watch = "/path/to/your/directory"  # Specify the directory to be monitored
    queue_file = 'file_event_queue.log'
    event_handler = FileEventWriter(queue_file)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)

    observer.start()
    print(f"Monitoring directory: {path_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
