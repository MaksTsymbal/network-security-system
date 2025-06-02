import os
import uuid
from datetime import datetime, timedelta
from app.cryptomodule.store import CryptoKey, database
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

async def generate_key(key_type: str):
    if key_type.upper() == 'AES':
        raw = os.urandom(32)
        record = {
            'id': str(uuid.uuid4()),
            'key_type': 'AES',
            'public_key': '',
            'encrypted_private_key': raw.hex(),
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(days=1),
            'status': 'active'
        }
        query = CryptoKey.insert().values(**record)
        await database.execute(query)
        return record
    raise ValueError("Unknown key type")

async def list_keys():
    query = CryptoKey.select()
    return await database.fetch_all(query)

async def rotate_aes_key():
    await database.execute(CryptoKey.update().where(CryptoKey.c.key_type=='AES').values(status='revoked'))
    return await generate_key('AES')
