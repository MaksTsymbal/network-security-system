import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_aes_gcm(plaintext: bytes, key: bytes) -> bytes:
    """
    Шифрує байти plaintext ключем key (AES-GCM).
    Повертає: nonce + ciphertext + tag.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext

def decrypt_aes_gcm(data: bytes, key: bytes) -> bytes:
    """
    Розшифровує data = nonce (12 байт) + ciphertext + tag.
    Повертає байти plaintext.
    """
    aesgcm = AESGCM(key)
    nonce = data[:12]
    ct_and_tag = data[12:]
    plaintext = aesgcm.decrypt(nonce, ct_and_tag, None)
    return plaintext
