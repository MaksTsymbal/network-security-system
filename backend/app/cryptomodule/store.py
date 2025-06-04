from sqlalchemy import Table, Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from databases import Database
from sqlalchemy import create_engine, MetaData
from app.core.config import DATABASE_URL

database = Database(DATABASE_URL)
metadata = MetaData()

CryptoKey = Table(
    'crypto_keys', metadata,
    Column('id', UUID, primary_key=True),
    Column('key_type', String),
    Column('public_key', Text),
    Column('encrypted_private_key', Text),
    Column('created_at', DateTime),
    Column('expires_at', DateTime),
    Column('status', String),
)

crypto_keys = CryptoKey

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
