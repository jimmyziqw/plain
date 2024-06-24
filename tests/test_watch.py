import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SimpleHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'File modified: {event.src_path}')
    
    def on_created(self, event):
        print(f'File created: {event.src_path}')
    
    def on_deleted(self, event):
        print(f'File deleted: {event.src_path}')

if __name__ == "__main__":
    path = "D:\\AFUNFOLDER\korero" 
    event_handler = SimpleHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    print(f"Monitoring directory: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
