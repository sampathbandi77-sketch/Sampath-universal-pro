from pydantic import BaseModel, Field

class RiskPreview(BaseModel):
    capital: float = Field(gt=0)
    risk_percent: float = Field(gt=0, le=2)
    entry: float = Field(gt=0)
    stop_loss: float = Field(gt=0)
    lot_size: int = Field(default=1, ge=1)

def calculate_position_size(data: RiskPreview) -> dict:
    distance = abs(data.entry - data.stop_loss)
    if distance <= 0: raise ValueError("Entry and stop-loss must differ.")
    risk_amount = data.capital * data.risk_percent / 100
    units = int(risk_amount // distance)
    quantity = (units // data.lot_size) * data.lot_size
    return {"risk_amount": round(risk_amount, 2), "stop_distance": round(distance, 4), "suggested_quantity": quantity, "estimated_risk": round(quantity * distance, 2), "note": "Risk estimate only; excludes slippage, brokerage, taxes and gaps."}
