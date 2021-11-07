### Notes for the reader

Be carefull to base64 encode your raw shellcode script before hosting it on localhost
Store the raw shellcode in /tmp/shellcode.raw
then run (on your linux shell):
user$ base64 -i shellcode.raw >
shellcode.bin
user$ python -m http.server 8000
