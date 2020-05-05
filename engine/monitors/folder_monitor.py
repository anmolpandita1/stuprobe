import sys
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent




class DirEventHandler(DirCreatedEvent):

    def __init__(self, path):
        self._src_path = path

    def dispatch(self, event):
        if event.__class__.__name__ == 'DirCreatedEvent':
            self.process(event)
            

    def process(self, event):
        created_folder_path =  event._src_path + "/"
        os.system("python \"" + sys.argv[2] + "\" \"" + created_folder_path  +"\"")





if __name__ == "__main__":

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = DirEventHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()