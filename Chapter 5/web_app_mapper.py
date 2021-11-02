import os
import queue
import threading
import urllib.error
import urllib.parse
import urllib.request

threads = 10
target = "http://www.test.com"

# here you should download your local copy of Joomla for testing purposes
directory = "/Users/user/Downloads/joomla-x.x.x"  

# filtering out the file extensions we don't need. Feel free to extend! 
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)
web_paths = queue.Queue()

for r, d, f in os.walk("."):
    for files in f:
        remote_path = f"{r}/{files}"
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f"{target}{path}"
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request)
            print(f"[{response.code}] => {path}")
            response.close()
        except urllib.error.HTTPError as e:
            print(f"Failed for error {e}, {e.code}") 

for thread in range(threads):
    print(f"Spawning thread: {thread}")
    t = threading.Thread(target=test_remote)
    t.start()      
