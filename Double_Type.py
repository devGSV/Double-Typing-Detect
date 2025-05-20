from pynput import keyboard
from datetime import datetime

THRESHOLD_WARN = 45  # زیر این مقدار، مشکوک به دبل تایپ

last_backspace_time = None
min_interval_ms = None

def on_press(key):
    global last_backspace_time, min_interval_ms
    if key == keyboard.Key.backspace:
        now = datetime.now()
        if last_backspace_time:
            delta = (now - last_backspace_time).total_seconds() * 1000

            if min_interval_ms is None or delta < min_interval_ms:
                min_interval_ms = delta
                if delta < THRESHOLD_WARN:
                    print(f"{delta:.2f} ms → Double Typing Detected!")
                else:
                    print(f"Record : {delta:.2f} ms")
        else:
            print("First Backspace")
        last_backspace_time = now

def on_release(key):
    if key == keyboard.Key.esc:
        print("\n Program Ended")
        if min_interval_ms:
            print(f"Min Delay -> {min_interval_ms:.2f} ms")
        else:
            print("Nothing")
        return False

print("Exit : ESC")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# C:\Users\Administrator\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\pyinstaller.exe --onefile --clean Double_Type.py