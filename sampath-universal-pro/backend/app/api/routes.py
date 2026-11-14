from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from ..brokers.registry import BROKERS
from ..strategies.engine import STRATEGIES
from ..execution.risk import RiskPreview, calculate_position_size

router = APIRouter(prefix="/api")

@router.get("/brokers")
def brokers(): return list(BROKERS.values())

@router.get("/strategies")
def strategies(): return STRATEGIES

@router.get("/market/demo")
def demo_market():
    return {"source":"SIMULATED_DEMO", "timestamp":"2026-11-14T09:15:00+05:30", "indices":[{"symbol":"NIFTY 50","price":0,"change_pct":0},{"symbol":"BANKNIFTY","price":0,"change_pct":0},{"symbol":"SENSEX","price":0,"change_pct":0}], "notice":"No live feed configured. Zero values are placeholders, not market prices."}

@router.post("/risk/preview")
def risk_preview(data: RiskPreview):
    try: return calculate_position_size(data)
    except ValueError as e: raise HTTPException(400, str(e))

class OrderPreview(BaseModel):
    broker: Literal["upstox","dhan","zerodha","angelone","coinswitch"]
    symbol: str = Field(min_length=1, max_length=80)
    side: Literal["BUY","SELL"]
    quantity: int = Field(gt=0)
    order_type: Literal["MARKET","LIMIT","SL","SL-M"]
    price: float | None = Field(default=None, gt=0)
    mode: Literal["MANUAL","AUTOMATED"] = "MANUAL"

@router.post("/orders/preview")
def order_preview(order: OrderPreview):
    return {"accepted_for_preview": True, "live_order_submitted": False, "order": order.model_dump(), "message":"Preview only. Live order execution is disabled in this starter build."}
