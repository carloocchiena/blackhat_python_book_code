### Notes for the reader

#### keylogger.py
This script requires `pyHook` library, that is not compatible with newer versions of Python. 

Check for details (and, in the case, updated answers on <a href="https://stackoverflow.com/questions/59968523/unable-to-install-pyhook-python-3-8-1">Stack Overflow - pyHook issues.</a>)<br>

You have two ways ahead:
- Search for a wheel file appropriate for the Python version you are running here https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook 
- Use <a href="https://libraries.io/pypi/pyWinhook">pyWinhook</a>, a pyHook fork with some updates for support latest Visual Studio compilers.<br> 
Two methods here:<br>
____ a) `pip install pyWinhook==1.6.2`<br>
____ b) `python -m pip install pyWinhook-1.6.2-cp38-cp38-win_amd64.whl`<br><br>

I would like to switch to `keyboard` module in order to bypass all this mess, but at the moment I am not able to reproduce the exact workflow offered by the book without going thru pyHook.<br>
ps. if the topic is of your interested, check my keylogger for Power Shell here: https://gist.github.com/carloocchiena/316234e45f67ca63f07620e15e7dfaef

#### shell_exec.py
Be carefull to base64 encode your raw shellcode script before hosting it on localhost<br>
Store the raw shellcode in /tmp/shellcode.raw<br>
then run (on your linux shell):<br>
`user$ base64 -i shellcode.raw >`<br>
`shellcode.bin`<br>
`user$ python -m http.server 8000`<br>
