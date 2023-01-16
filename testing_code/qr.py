import qrcode
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def create_qr_code(name, dob, private_key_pem, public_key_pem):
    # Load the private key and public key from their PEM representations
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Encrypt the name and date of birth using the private key
    name_ciphertext = private_key.encrypt(
        name.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    dob_ciphertext = private_key.encrypt(
        dob.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Generate a signature for the encrypted fields using the private key
    signature = private_key.sign(
        name_ciphertext + dob_ciphertext,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Create a QR code image with the encrypted fields and signature
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(name_ciphertext)
    qr.add_data(dob_ciphertext)
    qr.add_data(signature)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Return the QR code image and the public key
    return img, public_key

# Example usage
private_key_pem = b'-----BEGIN RSA PRIVATE KEY-----\n...'
public_key_pem = b'-----BEGIN RSA PUBLIC KEY-----\n...'
img, public_key = create_qr_code('John Smith', '01/01/1970', private_key_pem, public_key_pem)















import pyzbar
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def get_data_from_qr_code(img, public_key_pem):
    # Scan the QR code image to extract the data
    data = pyzbar.decode(img)[0].data

    # Split the data into the encrypted fields and the signature
    name_ciphertext, dob_ciphertext, signature = data[:256], data[256:512], data[512:]

    # Load the public key from its PEM representation
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Verify the signature using the public key
    public_key.verify(
        signature,
        name_ciphertext + dob_ciphertext,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Decrypt the name and date of birth using the public key
    name = public_key.decrypt(
        name_ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()
    dob = public_key.decrypt(
        dob_ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

    # Return the name and date of birth
    return name, dob

# Example usage
public_key_pem = b'-----BEGIN RSA PUBLIC KEY-----\n...'
name, dob = get_data_from_qr_code(img, public_key_pem)






# This function loads the public key from its PEM representation using the 
# serialization.load_pem_public_key() function, verifies the signature using the 
# public_key.verify() function, and decrypts the name and date of birth using the 
# public_key.decrypt() function. It then returns the decrypted name and date of birth as 
# strings.















def create_qr_code(fields, private_key_pem, public_key_pem):
    # Load the private key and public key from their PEM representations
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Encrypt the fields using the private key
    encrypted_fields = []
    for field in fields:
        encrypted_fields.append(
            private_key.encrypt(
                field.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        )

    # Create a QR code image with the encrypted fields and the public key
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    for encrypted_field in encrypted_fields:
        qr.add_data(encrypted_field)
    qr.add_data(public_key_pem)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Return the QR code image and the public key
    return img, public_key

# Example usage
private_key_pem = b'-----BEGIN RSA PRIVATE KEY-----\n...'
public_key_pem = b'-----BEGIN RSA PUBLIC KEY-----\n...'
fields = ['John Smith', '01/01/1970', '123 Main St']
img, public_key = create_qr_code(fields, private_key_pem, public_key_pem)









def get_data_from_qr_code(img, public_key_pem):
    # Scan the QR code image to extract the data
    data = pyzbar.decode(img)[0].data

    # Split the data into the encrypted fields and the signature
    encrypted_fields = data[:-768]
    signature = data[-768:]

    # Load the public key from its PEM representation
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Verify the signature using the public key
    public_key.verify(
        signature,
        b''.join(encrypted_fields),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Decrypt the fields using the public key
    fields = []
    for encrypted_field in encrypted_fields:
        fields.append(
            public_key.decrypt(
                encrypted_field,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode()
        )

    # Return the fields
    return fields

# Example usage
public_key_pem = b'-----BEGIN RSA PUBLIC KEY-----\n...'
fields = get_data_from_qr_code(img, public_key_pem)