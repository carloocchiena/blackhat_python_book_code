import win32con
import win32api
import win32security
import wmi
import os

LOG_FILE = "process_monitor_log.csv"

def get_process_privileges(pid):
    try:
        # obtain a handle to the target process
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION,
                                     False,
                                     pid)
        
        # open main process token
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)
        
        # retrieve the list of privileges enabled
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)
        
        # iterate over privileges and output the ones that are enabled
        priv_list = []
        for priv_id, priv_flags in privs:
            # check if privilege is enabled
            if priv_flags == 3:
                priv_list.append(win32security.LookupPrivilegeName(None, priv_id))
                
    except:
        priv_list.append("N/A")
        
    return "|".join(priv_list)

def log_to_file(message):
    with open(LOG_FILE, "ab") as fd:
        fd.write(f"{message}\r\n")
    return

# create a log file header
if not os.path.isfile(LOG_FILE):
    log_to_file("Time,User,Executable,CommandLine,PID,ParentPID,Privileges")
    
# instantiate the WMI interface
c = wmi.WMI()

# create our process monitor
process_watcher = c.Win32_Process.watch_for("creation")

while True:
    try:
        new_process = process_watcher()
        proc_owner = new_process.GetOwner()
        proc_owner = f"{proc_owner[0]}\\{proc_owner[2]}"
        create_date = new_process.CreationDate
        executable = new_process.ExecutablePath
        cmdline = new_process.CommandLine
        pid = new_process.ProcessId
        parent_pid = new_process.ParentProcessId
        
        privileges = get_process_privileges(pid)
        
        process_log_message = f"{create_date}, {proc_owner}, {executable}, {cmdline}, {pid}, {parent_pid}, {privileges}."
        
        print(f"{process_log_message}\r\n")
        
        log_to_file(process_log_message)
    except:
        pass
        