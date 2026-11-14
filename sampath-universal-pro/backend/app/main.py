from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .core.config import settings
from .api.routes import router

app = FastAPI(title=settings.app_name, version="0.1.0", description="Starter API. Live broker trading is disabled.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

# Setup Jinja2 templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    """Serve HTML landing page with Vercel Speed Insights"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": settings.app_name,
        "status": "running",
        "trading_mode": settings.trading_mode,
        "live_trading_enabled": settings.live_trading_enabled
    })

@app.get("/health")
def health(): return {"status":"ok"}
