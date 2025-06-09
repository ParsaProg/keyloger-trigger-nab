from pynput import keyboard
import subprocess
import threading
import keyboard as keyboardMain
import sys

# Constants
EXIT_KEY = "esc"
CMD_TRIGGER_KEYCODE = 173
EXIT_KEYCODE = 1  # KeyCode for '1' key (when using pynput)
EXIT_SCAN_CODE = 2  # Scan code for '1' key (when using keyboard module)

# --- pynput listener
def get_key_code(key):
    if isinstance(key, keyboard.KeyCode):
        return key.vk
    elif isinstance(key, keyboard.Key):
        return key.value.vk
    return None

def on_press_pynput(key):
    keyCode = get_key_code(key)
    print(f"Key pressed: {key} | Key code: {keyCode}")

    if keyCode == CMD_TRIGGER_KEYCODE:
        subprocess.Popen("cmd", creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif key == keyboard.Key.esc or keyCode == EXIT_KEYCODE:
        print("Exit key pressed (pynput). Exiting.")
        sys.exit()

def start_pynput_listener():
    with keyboard.Listener(on_press=on_press_pynput) as listener:
        listener.join()

# --- keyboard module listener
def on_key_event(e):
    print(f"Key Pressed: {e.name} | Scan Code: {e.scan_code}")

    if e.scan_code == -174:  # F1
        keyboardMain.send('up')
    elif e.scan_code == -175:  # F2
        keyboardMain.send('down')
    elif e.name == "esc" or e.scan_code == EXIT_SCAN_CODE:
        print("Exit key pressed (keyboard module). Exiting.")
        sys.exit()

def start_keyboard_listener():
    keyboardMain.on_press(on_key_event)
    keyboardMain.wait()

# --- Run both listeners
if __name__ == "__main__":
    threading.Thread(target=start_pynput_listener, daemon=True).start()
    start_keyboard_listener()
