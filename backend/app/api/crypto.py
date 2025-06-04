import ssl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID

from app.cryptomodule.store import database, CryptoKey
from app.crypto_utils import encrypt_aes_gcm, decrypt_aes_gcm

class EncryptRequest(BaseModel):
    key_id: UUID
    plaintext: str


class EncryptResponse(BaseModel):
    ciphertext: str


class DecryptRequest(BaseModel):
    key_id: UUID
    ciphertext: str


class DecryptResponse(BaseModel):
    plaintext: str

router = APIRouter()

async def _get_key_bytes(key_id: UUID) -> bytes:
    query = CryptoKey.select().where(CryptoKey.c.id == str(key_id))
    record = await database.fetch_one(query)
    if not record:
        raise HTTPException(status_code=404, detail="Ключ не знайдено")
    if record["status"] != "active":
        raise HTTPException(status_code=400, detail="Ключ неактивний")
    raw_key = bytes.fromhex(record["encrypted_private_key"])
    return raw_key


@router.post("/encrypt", response_model=EncryptResponse, summary="Зашифрувати текст AES-GCM")
async def encrypt_text(req: EncryptRequest):
    key_bytes = await _get_key_bytes(req.key_id)
    try:
        ciphertext_bytes = encrypt_aes_gcm(req.plaintext.encode("utf-8"), key_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {e}")
    return EncryptResponse(ciphertext=ciphertext_bytes.hex())


@router.post("/decrypt", response_model=DecryptResponse, summary="Розшифрувати текст AES-GCM")
async def decrypt_text(req: DecryptRequest):
    key_bytes = await _get_key_bytes(req.key_id)
    try:
        plaintext_bytes = decrypt_aes_gcm(bytes.fromhex(req.ciphertext), key_bytes)
        plaintext = plaintext_bytes.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {e}")
    return DecryptResponse(plaintext=plaintext)

@router.post("/handshake")
async def handshake():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("./certs/server.pem", "./certs/server.key")
    return {"tls": "params"}
