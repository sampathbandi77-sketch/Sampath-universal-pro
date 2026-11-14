from abc import ABC, abstractmethod
from typing import Any

class BrokerAdapter(ABC):
    """Normalized contract. Implement each method using the broker's official API."""
    broker_name: str

    @abstractmethod
    async def connection_status(self) -> dict[str, Any]: ...
    @abstractmethod
    async def get_profile(self) -> dict[str, Any]: ...
    @abstractmethod
    async def get_funds(self) -> dict[str, Any]: ...
    @abstractmethod
    async def get_positions(self) -> list[dict[str, Any]]: ...
    @abstractmethod
    async def get_orders(self) -> list[dict[str, Any]]: ...

    async def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Live order placement is not implemented in this starter.")
