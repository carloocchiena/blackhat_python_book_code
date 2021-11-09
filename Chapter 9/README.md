### Notes for the reader

- The cryptography library used in the book (`pycrypto`) is deprecated. I used `pycryptodome` instead (further readings: https://blog.sqreen.com/stop-using-pycrypto-use-pycryptodome/)
<br><br>
- `mitb.py` stands for "Man-in-the-Browser" :) and yes, the book built it for Internet Explorer. <br> Since it doesn't make sense to me to invest time to reproduce a test case on IE, I left out the testing of this part, evaluating only the correctness of the code by debugging runs in my IDE.

- `ie_exfil` had some issues related to the handling of the plaintext variable. While I am not still able to have a full working routine between all the files created for this chapter, and some tuning is still in progress, I found <a href="https://github.com/EONRaider/blackhat-python3/pull/2/commits/fcab6afc19fc4ea01b8c5c475e7b8c5e4b158df6">this commit</a> to be very usefull. 

