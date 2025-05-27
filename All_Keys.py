from pynput import keyboard
import time

# Time threshold (in milliseconds). If two consecutive presses of the same key occur faster than this,
# it's considered potential double-typing.
DOUBLE_TYPING_THRESHOLD_MS = 50  # You can adjust this value

# Dictionary to store the last press time for each key
# Structure: {key_identifier: timestamp_in_ms}
last_key_press_times = {}

# Dictionary to count the number of double-typing detections for each key
# Structure: {key_identifier: count}
double_typing_counts = {}


def get_key_identifier(key_event):
    """
    Returns a unique string identifier for the pressed key.
    For character keys, it's the character itself.
    For special keys (like Ctrl, Shift, Esc), it's the key name.
    """
    if hasattr(key_event, 'char') and key_event.char is not None:
        return key_event.char
    else:
        return str(key_event)


def on_press(key_event):
    """
    This function is called when any key is pressed.
    """
    global last_key_press_times, double_typing_counts

    current_time_ms = time.monotonic() * 1000
    key_id = get_key_identifier(key_event)

    if key_id in last_key_press_times:
        previous_press_time_ms = last_key_press_times[key_id]
        time_difference_ms = current_time_ms - previous_press_time_ms

        if time_difference_ms < DOUBLE_TYPING_THRESHOLD_MS:
            # Update the double-typing counter for this key
            double_typing_counts[key_id] = double_typing_counts.get(key_id, 0) + 1

            # Print a warning with details
            print(f"⚠️ Potential double-typing detected for key '{key_id}'! "
                  f"Time difference: {time_difference_ms:.2f} ms "
                  f"(Count for this key: {double_typing_counts[key_id]})")
        # else:
            # To avoid flooding the console, non-warning reports can be disabled.
            # print(f"Key '{key_id}' pressed. Time since last press: {time_difference_ms:.2f} ms")

    # Store the current press time for this key
    last_key_press_times[key_id] = current_time_ms


def on_release(key_event):
    """
    This function is called when any key is released.
    Used to exit the program.
    """
    if key_event == keyboard.Key.esc:
        print("\n--- Final Double-Typing Report ---")
        if double_typing_counts:
            sorted_counts = sorted(double_typing_counts.items(), key=lambda item: item[1], reverse=True)
            print(f"Double-typing detection threshold: {DOUBLE_TYPING_THRESHOLD_MS} ms")
            print("Keys suspected of double-typing:")
            for key_id, count in sorted_counts:
                print(f"  - Key '{key_id}': {count} times")
        else:
            print("No double-typing instances detected with the set threshold.")
        print("--- Program Terminated ---")
        # Returning False stops the listener.
        return False

# ------------ Program Start ------------
print("Double-typing detection program is running...")
print(f"Detection threshold: {DOUBLE_TYPING_THRESHOLD_MS} ms")
print("Press 'Esc' to see the final report and exit the program.")
print("-" * 30)

# Create and run the keyboard event listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except Exception as e:
        print(f"An error occurred while running the listener: {e}")

# C:\Users\Administrator\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\pyinstaller.exe --onefile --clean All_Keys.py