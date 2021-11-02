## Notes for the reader

Scapy for Python3 is commonly found under Kamene libs https://kamene.readthedocs.io/en/latest/introduction.html<br>

### About pic_carver.py 

The cv2 module is now replaced by open-cv python. See: <br>
- https://pypi.org/project/opencv-python/
- https://docs.opencv.org/master/

Another source cited in the book is https://fideloper.com/facial-detection; 
<br>here, you can also download the data for the training set: https://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml

If you're not familiar with open-cv module, this part will result quite bumpy (also, the book goes thru this section without much explanation, even saying that the check of all the warnings will be up to the reader). <br>

As a personal note, the use case proposed by the book - scan for faces in attached images - looks uninteresting. There would have been more interesting cases, such as understanding what type of attachment is attached to an email, or the size of it. Something to work on in the future.

At current date I had no time yet to deep test this part of the code, so I am leaving it up for the future.
                                                                                                                                                  

