import sys
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
from volatility.plugins.registry.registryapi import RegistryApi
from volatility.plugins.registry.lsadump import HashDump

memory_file = "Win10X64.vmem" # see README.md on how to get memory dumps

sys.path.append("/volatility3.1.0.0")

registry.PluginImporter()
config = conf.ConfObject()

config.parse_options()
config.PROFILE = "Win10X64"
config.LOCATION = f"file://{memory_file}"

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

registry = RegistryApi(config)
registry.populate_offsets()

sam_offset = None
sys_offset = None

for offset in registry.all_offsets:
    
    if registry.all_offsets[offset].endswith("\\SAM"):
        sam_offset = offset
        print("[*] System: 0x%08x" % offset)
        
    if sam_offset is not None and sys_offset is not None:
        config.sys_offset = sys_offset
        config.sam_offset = sam_offset
        hashdump = HashDump(config)
        
        for hash in hashdump.calculate():
            print(hash)
        break
    
if sam_offset is None or sys_offset is None:
    print("[*] Failed to find the system or SAM offsets")
