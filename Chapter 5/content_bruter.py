import queue
import threading
import urllib.error
import urllib.parse
import urllib.request

threads = 50
target_url = "http://testphp.vulnweb.com"
wordlist_file = "all.txt"
file_extensions = [".php", ".bak", ".orig", ".inc"]
resume = None
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

def build_wordlist(word_list_file):
    with open (word_list_file, "r") as l:
        raw_words = [line.rstrip("\n") for line in l]

    found_resume = False
    words = queue.Queue()

    for word in raw_words:
        if resume:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print(f"Resuming wordlist from: {resume}")
        else:
            words.put(word)
    return words

def dir_bruter(extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # check if there's a file extensions
        # if not it's a directory path
        if "." not in attempt:
            attempt_list.append(f"/{attempt}/")
        else:
            attempt_list.append(f"/{attempt}")
        
        # if we want to bruteforce extensions
        if extensions:
            for extension in extensions:
                attempt_list.append(f"/{attempt}{extension}")
            
        for brute in attempt_list:
            url = f"{target_url}{urllib.parse.quote(brute)}"
            try:
                headers = {"User-Agent": user_agent}
                r = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(r)
                if len(response.read()):
                    print(f"[{response.code}] => {url}")
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    print(f"!!! {e.code} => {url}")

word_queue = build_wordlist(wordlist_file)

for thread in range(threads):
    t = threading.Thread(target=dir_bruter, args=(file_extensions,))
    t.start()
