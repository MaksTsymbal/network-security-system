from fastapi import APIRouter, HTTPException
from app.cryptomodule.manager import generate_key, list_keys, rotate_aes_key

router = APIRouter()

@router.post("/generate")
async def api_generate(type: str):
    try:
        key = await generate_key(type)
        return key
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("")
async def api_list():
    return await list_keys()

@router.post("/rotate")
async def api_rotate():
    return await rotate_aes_key()
