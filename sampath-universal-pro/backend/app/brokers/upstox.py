"""upstox adapter scaffold. Implement only against the provider's current official API docs."""
from .base import BrokerAdapter

class Adapter(BrokerAdapter):
    broker_name = "upstox"
    async def connection_status(self):
        return {"broker": self.broker_name, "status": "NOT_CONFIGURED", "live_enabled": False}
    async def get_profile(self): raise NotImplementedError("Complete official authentication first.")
    async def get_funds(self): raise NotImplementedError("Complete official authentication first.")
    async def get_positions(self): raise NotImplementedError("Complete official authentication first.")
    async def get_orders(self): raise NotImplementedError("Complete official authentication first.")
