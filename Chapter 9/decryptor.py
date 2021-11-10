import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# private key is from keygen.py
private_key = """-----BEGIN RSA PRIVATE KEY-----\n
MIIEowIBAAKCAQEA4WAcB2b4/4DyX9fb2p18qy9JZYEr/GvVqbTyz9BZKpaA5yGa\n
digBPnv8BWL05x00KkSjO9BRR14SgzZNz5CFDG45ZJvcWmhsN+a2u1t3IBsINyXW\n
U2vaLKB92gNzoJXygaiErAbg1vfhYu/t6pLh/f3Tg01cQN6SPV3xcQbnb/qlYMdi\n
rflZsuTaHFARiG3gEZDn2cdrXlabXsB+7IIbXBb11UToP1XuvFStEhWaSSZj/BvV\n
vK4cCNNUK/de8mQX22wAopcESz0o5JEs3Ka4slwkpB7KRYSgWcJqUEQWERiYNS9s\n
u1wZP71coqQthlbe1ce1yD8xBRl0Xc767DhKMwIDAQABAoIBAF4ORJRIQpkq4Lvj\n
84JIYEt2uAxO/KLjA+/Hrt/QhS3TUqdi7DnsVxyTFKnQ0wESvH75VyAyv4DnvxUY\n
WB/MIeJ+q6ATtcHbO3KW6+LD+LKi5WpSdaAp7grazbrq3toBSgwXXosGcdX07BBk\n
ridLtlnQEPIGmn4OBPzsVENFzNd7e/yEbtoy7QD/mRq839IyfS9eqBeBFOX6pGcN\n
2dmp6EkOREuK7JnPEyvrQwJc/ktKeUuCV63N9lZRLDUQI5yVIma3pJ01g5xHn+Lg\n
HY/wJAuqaLzmBTH95qEEe4G2m3QoVWDhO91qBJnSBDhW3oGHDFufCeKRcTODcrKF\n
f6KIBQ0CgYEA69JOSBDU0qNsRor9hXvv2PRLfd7QFmKtOlSpAHpUIimTltmR8Esh\n
WEs6288ZIWtiSb5kX70waw6yMY1hbo/aNj76y0uJGK0jfKU+me3/drVV11MquC6i\n
u96u2YfJ8gVaV2a3v+UH9EWuSC/zUFPkQYLLQf7ySK80ZxmKEEPBCmcCgYEA9Kj7\n
NEN8TbQF6T21wfAs64byXjMFewCxNudV9815cE7azJ0a6hgkMtLaNSxtvFgnkMMN\n
icY2F0KghQOWAL1JMwe9aNSmZpdCuC5rHcvcRKTMRDJc0msEr+R7lS4zQ/hjhGgt\n
CoUTalcki+3wANJ0uyEhloLGTc2BJDe2Ac9HulUCgYEAiLw4h7C6tifr8DtHJM7o\n
E3QTEbjQDyrIJrpQA+bqQaS53w3ogNwPSZLVXf6HI8mQBBJRQPIB0RGEYRcJF4Jx\n
lGKQKLBznctGeE+YLMjDB6G9VEz0yDbCRQypdZg2kA5qg6MbiDjUk96TX2fuPPVn\n
tFSSZoHdGif8yosUcrnWhKECgYAu6S+xZ7cv1vLDNBfjpb+XMXrLYREN8qYIFvc+\n
2mEMjbIaRY1hkVtve0pno6suz+BWO3AfGKhKcXYByxw57BFa/YLt1MhLJ3mdgxj6\n
z5ned5LLCLUPi4GMkEy53+/oennqa2cnezirzSWuxuKb5b6IGuQrzctkI6E9Zok5\n
c5sXOQKBgEPujIFHmXGaObsD3M/XURUCViRxE818dUctPfK2P+OJr5blOi8iHX+y\n
rpemIiq/4FLBBCJGyjNPCs8OA76RK6tqZ0W4AdvU7jStNEIaV9APdSur/VHTzC7k\n
9RTMA8AqBx4A4h++EKiPAsxPMiT6M6UXM69eIx1ExEIr5B1LTxSM\n
-----END RSA PRIVATE KEY-----"""

rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

offset = 0
decrypted = ""
encrypted = base64.b64encode(encrypted)

while offset < len(encrypted):
    decrypted += rsakey.decrypt(encrypted[offset:offset + 256])
    offset += 256
    
# now decompress to original
plaintext = zlib.decompress(decrypted)

print(plaintext)
