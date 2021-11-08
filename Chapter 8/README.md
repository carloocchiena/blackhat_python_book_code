### Notes for the reader

#### shell_exec.py
Be carefull to base64 encode your raw shellcode script before hosting it on localhost<br>
Store the raw shellcode in /tmp/shellcode.raw<br>
then run (on your linux shell):<br>
`user$ base64 -i shellcode.raw >`<br>
`shellcode.bin`<br>
`user$ python -m http.server 8000`<br>
