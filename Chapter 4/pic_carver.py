import cv2
from kamane.all import *

pictures_directory = "pic_carver/pictures"
faces_directory = "pic_carver/faces"
pcap_file= "bhp.pcap"

def face_detect(path, file_name):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface.alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False
    rects[:, 2] += rects[:, :2]

    # highlights the faces in the image
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1,y1), (x2,y2), (127,255,0), 2)
        cv2.inwrite(f"{faces_directory} {pcap_file} {file_name}, img")
    return True

def get_http_headers(http_payload):
    try:
        headers_raw = http_payload[:http_payload.index("\r\n\r\n") +2]
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw))
    except:
        return None
    if "Content-Type" not in headers:
        return None
    return headers

def extract_image(headers, http_payload):
    image = None
    image_type = None

    try:
        if "image" in headers["Content-Type"]:
            image_type = headers["Content-Type"].split("/")[1]
            image = http_payload[http_payload.index("\r\n\r\n") + 4:]
            # try to decompress the image if needed
            try:
                if "Content-Encoding" in list(headers.keys()):
                    if headers["Content-Encoding"] == "gzip":
                        image = zlib.decompress(image, 16 + zlib.MAX_WBITS)
                    elif headers["Content-Encoding"] == "deflate":
                        image = zlib.decompress(image)
            except:
                pass
    except:
        return None, None

    return image, image_type

def http_assembler(pcap_fl):
    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_fl)
    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # reassemble the stream into a single buffer
                    http_payload += str(packet[TCP].payload)
            except:
                pass
        
        headers = get_http_headers(http_payload)

        if headers is None:
            continue

        image, image_type = extract_image(headers, http_payload)

        if image is not None and image_type is not None:
            file_name = f"{pcap_fl}-pic_carver_{carved_images}.{image_type}"
            with open(f"{pictures_directory}{file_name}, 'wb'") as fd:
                fd.write(image)
            carved_images += 1

            #  now attempt face detection
            try:
                result = face_detect(f"{pictures_directory}, {file_name}", file_name)
                if result:
                    face_detected += 1
            except:
                pass
    
    return carved_images, faces_detected

carved_img, faces_dtct = http_assembler(pcap_file)

print(f"Exctracted: {carved_images} images")
print(f"Detected: {face_detected} faces")







