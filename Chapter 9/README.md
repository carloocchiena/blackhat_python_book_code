### Notes for the reader

- The cryptography library used in the book (`pycrypto`) is deprecated. I used `pycryptodome` instead (further readings: https://blog.sqreen.com/stop-using-pycrypto-use-pycryptodome/)

- `mitb.py` stands for "Man-in-the-Browser" :) and yes, the book built it for Internet Explorer. <br> Since it doesn't make sense to me to invest time to reproduce a test case on IE, I left out the testing of this part, evaluating only the correctness of the code by debugging runs in my IDE.

- `ie_exfil` had some issues related to the handling of the plaintext variable. While I am not still able to have a full working routine between all the files created for this chapter, and some tuning is still in progress, I found <a href="https://github.com/EONRaider/blackhat-python3/pull/2/commits/fcab6afc19fc4ea01b8c5c475e7b8c5e4b158df6">this commit</a> to be very useful. The login to Tumblr is not working at the moment, however I am skipping testing this part since digging around Tumblr DOM seems to be quite out of scope at least in the contingency. Depending on your running env, tweak conveniently the main loop at the end of the script. Probably you don't really want it to scan your whole hard disk searching for docs.

- `cred_server.py` requires manual approval by firewall on Win10, so it is currently of little use.

- As a personal opinion, this section of the book seems outdated already for the publication date of the book.

