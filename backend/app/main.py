from prometheus_client import start_http_server, Counter, Histogram, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
import time
from app.api import keys, crypto
from app.cryptomodule.store import database

app = FastAPI()
app.include_router(keys.router, prefix="/keys")
app.include_router(crypto.router, prefix="/crypto")


REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests",
                        ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds",
                            "Request latency in seconds",
                            ["method", "endpoint"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    endpoint = request.url.path
    REQUEST_LATENCY.labels(request.method, endpoint).observe(latency)
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    return response

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(data, media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()
