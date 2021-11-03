import base64
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request

from burp import IBurpExtender
from burp import IContextMenuFactory
from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem

bing_api_key = "YOUR_API_KEY"

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        #setting up extensions
        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)
        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))
        return menu_list

    def bingMenu(self, event):
        # grab the details of what the user clicked
        http_traffic = self.context.getSelectedMessages()
        print(f"{len(http_traffic)} requests highlighted")

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            print(f"User selected host: {host}")
            self.bing_search(host)
        return

    def bingSearch(self, host):
        # check if we have an IP or hostname
        is_ip = re.match(r'[0-9]+(?:\.[0-9]+){3}', host)

        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True

        bing_query_string = f"'ip:{ip_address}'" 
        self.bing_query(bing_query_string)

        if domain:
            bing_query_string = f"'domain:{host}'"
            self.bing_query(bing_query_string)    

    def bingQuery(self, bing_query_string):

        print(f"Performing Bing search: {bing_query_string}")

        quoted_query = urllib.parse.quote(bing_query_string)

        http_request = f"GET https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$top=20&Query={quoted_query} HTTP/1.1\r\n"
        http_request += "Host: api.datamarket.azure.com\r\n"
        http_request += "Connection: close\r\n"
        http_request += "Authorization: Basic %s\r\n" % base64.b64encode(":%s" % bing_api_key)
        http_request += "User-Agent: Pentesting Python\r\n\r\n"

        json_body = self._callbacks.makeHttpRequest("api.datamarket.azure.com", 443, True, http_request).tostring()

        json_body = json_body.split("\r\n\r\n", 1)[1]

        try:
            r = json.loads(json_body)
            if len(r["d"]["results"]):
                for site in r["d"]["results"]:
                    print("*" * 100)
                    print(site['Title'])
                    print(site['Url'])
                    print(site['Description'])
                    print("*" * 100)
                    j_url = URL(site['Url'])
                    if not self._callbacks.isInScope(j_url):
                        print("Adding to Burp scope")
                        self._callbacks.includeInScope(j_url)
        except:
            print("No results from Bing")
               
        return