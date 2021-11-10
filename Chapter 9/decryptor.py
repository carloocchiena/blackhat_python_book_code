import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# paste here the encrypted code you got from ie_exfil.py (and that should have been posted to Tumblr as well)
encrypted = b'jyBM2jcAyS7asGBjoZGYl/YlutS1HBs3s/JPFMPtTa5UOjseCdC9loraG5CkK43z90qSr+Jcp+4xtAl1bhBcZgEUifO82m/4+6z6cfd7X9DEHjwiAorb51rQ2+iOwrwwgcmEqXK/enTJ1DPdD8O/f8UB0z1Cvl2LEwrmZe0RTdCR8UILZhy39BWLPVFm7Chgg96Yp2rYQgpU8ObtwChDlst58B1oltZKn8LVbkapy5MO6214R0HlOHhJglbK3Ok+sINqdDAQRdZ9rOIbe1hVthJmqneZyR2PdTbtmTir3Q+3SkskYuayFwL7dTW1VJEfKBrbaYQU14A1rECrkFAxXQ=='

# private key is from keygen.py
private_key = b"""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAuO+ZrmxOCIYrdmbS3io0MQ3dL3/r5AVZdXr5RfwnVXoGvoX7
ABhJjovpIJvAR19U8PuADbE+WpjCZsP0yH//Bzi5zcn1dgkIpqHcD7UUb9x8k9Lh
MyD6neqwXe6VmxdJXl9NWYTmzQDdOLw4ms0B9yYLKtWURAwP4Yo+0ZmOdCkBBKBL
yv1G6ndw8oeeTBNsPa6QsrNZPfL3r6CkkBh9eb1jnlUt6I+2qjqsX+N5ccHEPMXY
FSMJVXiZecELlwILLxMU++R/717wzxYc1h66AStJTXvL6LiTOvtTCUPyJk2S9EVj
HfCjBLYR1Rq0rnouxafllr98u/U+ZOQQ4luVDQIDAQABAoIBADDdWlGMm3fEH9LK
q3f5Vc4KWEG3PriCs1cH1bqovCnpMsP/uckWIcVw8XnkvYL+TP7ZrUWw6gVdLKyj
pVee/l9FnU6jSODV1TvWM8PQuGQwMZiLlWaBlcbJHq3LHyuaFRBDBTiclbFgQ5O8
pAY/GgBYRIYeZe0u9LlG4n9WYB4PzdlLrnPAg4d+1gdiXClR0irlBNz9gOQGHjb7
w8pbOLDNKrnii6tSm4tXWTLE0VGIRu9ex/C/tFuFbOXr6IJw05w1ylfLCO0dDBZC
0ArqSVrlV4hfwUHvmowyysgxQYlsL+r1+RmdxX3feVrGUWwWbmm8eaufg3lpl5Gl
qSw0Yy8CgYEAwpJj9a3GqFuhb/xWQi2otnU3zEss3FEN8eS01+BajESg/DwpfkvY
sci8kQqUqKCltKOMXuWknhWs3T9GjQDhZ9fPyhut/U8mIPdHMlux3uCAmZxbdHh3
+cRF6gUBBKm79dogaJFszRwfwIFzvYfvQYGK6R+GOs+UKawI0ZIv+7sCgYEA81Jr
xA+GNcWRGNsppGK/MOt2GR8h0EKSoVJn1G5pwaIvtfcB/tbgeWX/3n89xNgnD3ab
BK7aL73uwFr1/X2xUR8UTVQj5uDqUMI7rJ7Ngc9TFG50mybiKYKxbwimz0JH/INi
DmMbqVOVeqLFe7WAjHm2eIVPSJtMMwwOGR8rUdcCgYBzGENW/a+IwYMyijLAPOAS
5i3WhBWKUcwM7bvoAwes95++9RuaYOVS7SpWJcsgIL9EpoYPUIpbFPlHevmRyRaM
5cU9ibgXIm2sjHmqGUGTVHvd4fbbY7OcpHSy5LjgeEL+QERxdqzEe8Fwj2LWl4V4
21c/ZW1ydn3vVJt21KHbpwKBgQDxdzCkz7cjc52LaisIDEqp9HEtevymXPqAh3Os
l6nx086/KJJdYMZBExz5o5Ib31nb+Zra6d5ylGzzjREi73JhC5OtLbu3Kiq93BM2
Oh29HY7X7slfExZLlXwZsR9A/QjNKWDM4EOaJO1pV1DddIBOZ5bSQZEtf5f97I+t
FIZ73wKBgEcWcS/ZFDct/LDTYpjS2AER8r20buDewRlUXF4R5xrQRQGRugj5vpUg
PL93p45a6J5mxq6Ove73aXeDW9q+SxShKfC01agFYWoZybEawqeinM1SecLxMIKO
mjn+BsAxbuxAvsbLXqErzulOmy4Oql8ewWvJmIv6u03+7/Xrv1Hk
-----END RSA PRIVATE KEY-----"""

rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

chunk_size = 256
offset = 0
decrypted = ""
encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted += str(rsakey.decrypt(encrypted[offset:offset + chunk_size]))
    offset += chunk_size
    
# now decompress to original
plaintext = zlib.decompress(decrypted)

print(plaintext)