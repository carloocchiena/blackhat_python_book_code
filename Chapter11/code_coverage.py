import sys
sys.path.append('C:/Program Files (x86)/Immunity Inc/Immunity Debugger')
sys.path.append('C:/Program Files (x86)/Immunity Inc/Immunity Debugger/Libs')

from immlib import *

class CcHook(LogBpHook):
    def __init__(self):
        LogBpHook.__init__(self)
        self.imm = Debugger()
        
    def run(self, regs):
        self.imm.log("%08x" % regs['EIP'], regs['EIP'])
        self.imm.deleteBreakpoint(regs["EIP"])
        return
    
def main(args):
    imm = Debugger()
    
    calc = imm.getModule("calc.exe")
    imm.analyseCode(calc.getCodebase())
    
    functions = imm.getAllFunctions(calc.getCodebase())
    
    hooker = CcHook()
    
    for function in functions:
        hooker.add("%08x" % function, function)
        
    return f"Tracking {len(functions)} functions"
    