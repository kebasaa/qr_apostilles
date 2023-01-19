import json
import base64
import zlib
import hmac
from hashlib import sha256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

def sign_json(json_str, private_key):
    json_bytes = json.dumps(json_str).encode()
    base64_bytes = base64.b64encode(json_bytes)
    compressed_bytes = zlib.compress(base64_bytes)
    signature = private_key.sign(compressed_bytes, padding.PKCS1v15(), hashes.SHA256())
    return signature, compressed_bytes

def verify_signature(signature, json_bytes, public_key):
    try:
        public_key.verify(signature, json_bytes, padding.PKCS1v15(), hashes.SHA256())
        return True
    except:
        return False

# Example usage
json_str = {"example_key": "example_value"}
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

signature, compressed_bytes = sign_json(json_str, private_key)

verification_result = verify_signature(signature, compressed_bytes, public_key)
print("Signature Verification: ",verification_result)