from .base import BrokerAdapter

BROKERS = {
    "upstox": {"name": "Upstox", "auth": "OAuth 2.0", "status": "NOT_CONFIGURED", "market": "India equities/F&O"},
    "dhan": {"name": "Dhan", "auth": "DhanHQ authorization", "status": "NOT_CONFIGURED", "market": "India equities/F&O"},
    "zerodha": {"name": "Zerodha", "auth": "Kite Connect login flow", "status": "NOT_CONFIGURED", "market": "India equities/F&O"},
    "angelone": {"name": "Angel One", "auth": "SmartAPI session", "status": "NOT_CONFIGURED", "market": "India equities/F&O"},
    "coinswitch": {"name": "CoinSwitch", "auth": "API key + signed requests", "status": "NOT_CONFIGURED", "market": "Crypto (separate module)"},
}

class AdapterRegistry:
    def __init__(self): self._adapters: dict[str, BrokerAdapter] = {}
    def register(self, name: str, adapter: BrokerAdapter): self._adapters[name] = adapter
    def get(self, name: str) -> BrokerAdapter:
        if name not in self._adapters: raise KeyError(f"{name} adapter is not configured")
        return self._adapters[name]

registry = AdapterRegistry()
