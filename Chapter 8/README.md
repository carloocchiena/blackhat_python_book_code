### Notes for the reader

### keylogger.py
This script requires `pyHook` library, that is not compatible with newer versions of Python. 
You have two way ahead:
- search for a wheel file appropriate for the Python version you are running here https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook 
- use <a href="https://libraries.io/pypi/pyWinhook">pyWinhook</a>, a pyHook fork with some updates for support latest Visual Studio compilers. Two methods here:<br>
    a) `pip install pyWinhook==1.6.2`<br>
    b) `python -m pip install pyWinhook-1.6.2-cp38-cp38-win_amd64.whl`<br>
I would like to switch to `keyboard` module in order to bypass all this mess, but at the moment I am not able to reproduce the exact workflow offered by the book without going thru pyHook.

#### shell_exec.py
Be carefull to base64 encode your raw shellcode script before hosting it on localhost<br>
Store the raw shellcode in /tmp/shellcode.raw<br>
then run (on your linux shell):<br>
`user$ base64 -i shellcode.raw >`<br>
`shellcode.bin`<br>
`user$ python -m http.server 8000`<br>
