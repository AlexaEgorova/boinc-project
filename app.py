"""Telemetry Server API."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    store_router,
    user_router
)

app = FastAPI(
    title="Gimmefy API",
    openapi_url="/zpg/openapi.json",
    docs_url="/zpg/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(store_router.router)
app.mount("/zpg/assets", StaticFiles(directory="assets"), name="assets")
