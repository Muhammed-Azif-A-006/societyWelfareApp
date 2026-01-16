# Automatic App Restart on Code Modification

For a smoother development experience, you can set up your application to automatically restart when changes are made to the code. This can be achieved using a file monitoring tool. For Python projects, `watchdog` is a good option.

## Setup Instructions

1.  **Install `watchdog`**:
    If you don't have `watchdog` installed, you can install it using pip:
    ```bash
    pip install watchdog
    ```

2.  **Create a Watchdog Script**:
    Create a new Python file (e.g., `watch_and_run.py`) in your project's root directory with the following content:

    ```python
    import time
    import os
    import subprocess
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class MyEventHandler(FileSystemEventHandler):
        def __init__(self, script_to_run):
            super().__init__()
            self.script_to_run = script_to_run
            self.process = None
            self._start_app()

        def _start_app(self):
            if self.process:
                self.process.terminate()
                self.process.wait()
                print("--- App terminated ---")
            print(f"--- Starting {self.script_to_run} ---")
            self.process = subprocess.Popen(["streamlit", "run", self.script_to_run])

        def on_modified(self, event):
            if not event.is_directory and event.src_path.endswith('.py'):
                print(f"File modified: {event.src_path}. Restarting app...")
                self._start_app()

    if __name__ == "__main__":
        path = "."  # Monitor current directory
        script_to_run = "app.py" # Your main Streamlit app file

        event_handler = MyEventHandler(script_to_run)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        if event_handler.process:
            event_handler.process.terminate()
            event_handler.process.wait()
            print("--- App terminated ---")
    ```

3.  **Run the Watchdog Script**:
    Open your terminal in the project's root directory and run the watchdog script:

    ```bash
    python watch_and_run.py
    ```

    This script will start your `app.py` using `streamlit run` and automatically restart it whenever a Python file in the current directory (or subdirectories if `recursive=True`) is modified.

    To stop the watchdog script, press `Ctrl+C` in the terminal where it's running.
