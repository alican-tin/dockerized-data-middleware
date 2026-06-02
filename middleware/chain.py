from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from regex_utils import apply_all_masks

class Handler(ABC):
    def __init__(self):
        self._next_handler: Optional['Handler'] = None

    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        if self._next_handler:
            return self._next_handler.handle(log_data)
        return log_data

class PerformanceFilterHandler(Handler):
    def handle(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        if log_data.get("log_level") in ["INFO", "WARNING"]:
            return {"status": "ignored", "reason": "Log level skipped due to performance rules"}
        return super().handle(log_data)

class SecurityMaskingHandler(Handler):
    def handle(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        if "payload" in log_data:
            log_data["payload"] = apply_all_masks(log_data["payload"])
        return super().handle(log_data)

class EnrichmentHandler(Handler):
    def handle(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        log_data["islenen_zaman"] = datetime.now(timezone.utc).isoformat()
        log_data["islem_sunucusu"] = "Node-1"
        return super().handle(log_data)