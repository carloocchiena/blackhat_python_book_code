import re
from datetime import datetime
from html.parser import HTMLParser

from burp import IBurpExtender
from burp import IContextMenuFactory
from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL


class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

    def handleData(self, data):
        self.page_text.append(data)

    def handleComment(self, data):
        self.handle_data(data)

    def strup(self, html):
        self.feed(html)
        return " ".join(self.page_text)

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()

        # start with a common one
        self.wordlist = {"password"}

        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)
        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Create Wordlist", actionPerformed=self.wordlist_menu))
        return menu_list

    def wordlistMenu(self, event):
        # grab the details of what the user clicked
        http_traffic = self.context.getSelectedMessages()

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            self.host.add(host)
            http_response = traffic.getResponse()
            if http_response:
                self.get_words(http_response)
        self.display_wordlist()
        return

    def getWords(self, http_response):
        headers, body = http_response.tostring().split("\r\n\r\n", 1)

        # skip non-text responses
        if headers.lower().find("context-type: text") == -1:
            return

        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)    
        words = re.findall(r'[a-zA-Z]\w{2,}', page_text)

        for word in words:
            # filter out long strings
            if len(word) <= 12:
                self.wordlist.add(word.lower())
            return
    
    @staticmethod
    def mangle(word):
        year = datetime.now().year
        suffixes = ['', '1', '!', year]
        mangled = []
        for password in (word, word.capitalize()):
            for suffix in suffixes:
                mangled.append(f"{password}, {suffix}")
        return mangled
    

    def display_wordlist(self):
        print(f'# BHP Wordlist for site(s) {", ".join(self.hosts)}')
        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)
        return
