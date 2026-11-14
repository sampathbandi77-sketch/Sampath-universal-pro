from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.routes import router

app = FastAPI(title=settings.app_name, version="0.1.0", description="Starter API. Live broker trading is disabled.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root(): return {"app": settings.app_name, "status":"running", "trading_mode":settings.trading_mode, "live_trading_enabled":settings.live_trading_enabled}

@app.get("/health")
def health(): return {"status":"ok"}
