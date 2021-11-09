from Crypto.PublicKey import RSA

new_key = RSA.generate(2048)

public_key = new_key.public_key().exportKey("PEM")
private_key = new_key.exportKey("PEM")

print(f"Public Key: {public_key}")
print()
print(f"Private Key: {private_key}")
