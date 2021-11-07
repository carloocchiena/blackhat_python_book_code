import ctypes
import random
import time
import sys

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

keystrokes = 0
mouse_clicks = 0
double_clicks = 0

class LastInputInfo(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

def get_last_input():
    struct_lastinputinfo = LastInputInfo()
    struct_lastinputinfo.cbSize = ctypes.sizeof(LastInputInfo)

    # get last input registered
    user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))

    # now determine how long the machine has been running
    run_time = kernel32.GetTickCount()
    elapsed = run_time - struct_lastinputinfo.dwTime
    print(f"[*] It's been {elapsed} milliseconds since the last input event")
    return elapsed

def get_key_press():
    global mouse_clicks
    global keystrokes

    for code in range(0, 0xff):
        if user32.GetAsyncKeyState(code) == -32767:
            # 0x1 is the code for left mouse click
            if code == 1:
                mouse_clicks += 1
                return time.time()
            else:
                keystrokes += 1
    return None

def detect_sandbox():
    global mouse_clicks
    global keystrokes

    max_keystrokes = random.randint(10, 25)
    max_mouse_clicks = random.randint(5, 25)

    double_clicks = 0
    max_double_clicks = 10
    double_clicks_threshold = 0.250
    first_double_click = None

    average_mousetime = 0 # this var is never used in the book even if defined 
    max_input_threshold = 30000

    previous_timestamp = None
    detection_complete = False

    last_input = get_last_input()

    # exit if we hit our threshold
    if last_input >= max_input_threshold:
        sys.exit()

    while not detection_complete:
        keypress_time = get_key_press()
        if keypress_time is not None and previous_timestamp is not None:

            # calculate the time between double clicks
            elapsed = keypress_time - previous_timestamp

            # the user dobule clicked
            if elapsed <= double_clicks_threshold:
                double_clicks += 1

                if first_double_click is None:
                    # grab timestamp of the first double click
                    first_double_click = time.time()
                else:
                    # did they want to emulate a rapid succession of clicks?
                    if double_clicks == max_double_clicks:
                        if keypress_time - first_double_click <= (
                                max_double_clicks * double_clicks_threshold):
                            sys.exit()

            # we are happy there's enough user input
            if keystrokes >= max_keystrokes \
                    and double_clicks >= max_double_clicks \
                    and mouse_clicks >= max_mouse_clicks:
                return
            previous_timestamp = keypress_time

        elif keypress_time is not None:
            previous_timestamp = keypress_time

detect_sandbox()
print("We are ok!")
                