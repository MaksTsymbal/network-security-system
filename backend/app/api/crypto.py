import ssl
from fastapi import APIRouter

router = APIRouter()

@router.post("/handshake")
async def handshake():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("./certs/server.pem", "./certs/server.key")
    return {"tls": "params"}
