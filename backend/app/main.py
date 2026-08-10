from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import health, port_scanner, log_parser, file_integrity, auth, alerts,threats

app = FastAPI(
    title="AI SOC Platform API",
    version="0.1.0",
    description="Backend for the AI-powered Security Operations Center dashboard.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(port_scanner.router)
app.include_router(log_parser.router)
app.include_router(file_integrity.router)
app.include_router(auth.router)
app.include_router(alerts.router)
app.include_router(threats.router)