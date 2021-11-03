# Code and exercises from the book "Black Hat Python: Python Programming for Hackers and Pentesters" 
Examples, source code and exercises from the book "Black Hat Python" by Justin Seitz.

![image](https://user-images.githubusercontent.com/57464184/138901408-984413ab-2648-4dbe-b40c-37ac7b59fc63.png)

--------------------------------
### About the book
The book is a sort of a milestone for the pentesting world in Python.<br>
Although it was published relatively recently (2014), it is all written in Python 2.7.<br>

You can find the book on <a href="https://www.amazon.it/Black-Hat-Python-Programming-Pentesters-ebook/dp/B00QL616DW#customerReviews">Amazon</a>. <br>

While the official book page is on <a href="https://nostarch.com/black-hat-python2E#updates">No Starch Press</a> website.<br>

Apparently you should be able to download the book's source code from there, but the link atm is not working.<br>
 
### Reason for this repo
I quite enjoyed the book, but being written in Python 2.7 make it severely outdated.<br>

Deliberately, as expressed by the author, the scripts are written _raw & dirty_ to simulate the "as long as it works" approach during a penetration testing.<br>
However, this sometimes leads to code that is not very understandable, and not very efficient.<br>

Since I had to convert all the source codes anyway, to run them on my machine (Kali Linux VM + Win10 OS + Win10 VM + Python 3.9) I decided to go extra-mile and save them in a repo, in the meantime trying to optimize the code and making it a little more elegant (syntax, forms, error catching, unsupported libraries, naming conventions of both files and variables).

I starred this awesome repo from EONRaider for reference, that I might use in the case I'll be getting stuck in later sections of the books. Seems fair to add this source as a source of inspiration: <a href="https://github.com/EONRaider/blackhat-python3">EON RIDER Repo</a>

The code in the book does not always run flawlessy. It may depends on the local configuration on your machine, the test you are running, and also, outdated code presented in the book. So expect a bit of tweak here and there.<br> As a rule of thumb I found of great help the many <a href="https://stackoverflow.com/search?q=black+hat+python+book">threads already opened on Stack Overflow</a>. Some good advices also from <a href="https://medium.com/search?q=black%20hat%20python">Medium Black Hat Python</a>.

### Improvement made from the book's code
- Refactoring to Python 3 and code testing (unless otherwise specified)
- Update to PEP8 standards
- Upgraded readability (es. comments, indentation, variables name)
- Update of obsolete methods (es. print -s %)
- Better context management (es. open with, server.close()) 
- Disregard of unsupported libs 
- Minor tweaks and bugs found while testing the code 
- Search for additional files requested throughout the book and not provided, or provided at outdated links, and included in individual chapters.

### What you'll find in the repo
Chapter summary and titles are my own, for clarity. The book uses different titles and has no chapter summary.

#### Chapter 1: Intro
- This is an introductory chapter and it's mostly about installing Linux VM and Python. No coding here.

#### Chapter 2: Networking basics
- bhp_net.py
- bhp_server.py
- bhp_reverse_ssh_cmd.py
- bhp_ssh_cmd.py
- rforward.py
- tcp_server.py
- tcp_client.py
- tcp_proxy.py
- udp_client.py
- test_rsa.key

#### Chapter 3: Sniffing Tools
- scanner.py
- sniffer.py
- sniffer_ip_header_decode.py
- sniffer_with_icmp.py

#### Chapter 4: Scapy & ARP Poisoning (with an extra flavour of image reco)
- arper.py
- mail_sniffer.py
- pic_carver.py

#### Chapter 5: CMS Brute Force
- content_bruter.py
- joomla_killer.py
- web_app_mapper.py

#### Chapter 6: Burp Suite Integrations 
- bhp_bing.py
- bhp_fuzzer.py
- bhp_wordlist.py

### Contributions
All contributions are generally welcome :).<br>
Since I have not (yet?) made a specific routine for that, please follow a best-practice, common-sense based approach, opening an Issue first and starting a discussion on the change you'd wish to make.<br>
As a starting point, in each chapter folder I stated any known issues if any. <br>

