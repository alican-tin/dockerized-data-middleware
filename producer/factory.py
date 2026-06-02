import random
import string
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any

LOG_LEVELS = ["INFO", "WARNING", "ERROR", "FATAL"]

def _generate_tckn() -> str:
    return "".join(random.choices(string.digits, k=11))

def _generate_cc() -> str:
    return "".join(random.choices(string.digits, k=16))

def _generate_email() -> str:
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "exchange.local"]
    user = "".join(random.choices(string.ascii_lowercase, k=8))
    return f"{user}@{random.choice(domains)}"

class LogProduct(ABC):
    """Abstract Log Product"""
    @abstractmethod
    def generate(self) -> Dict[str, Any]:
        pass

class TransactionLog(LogProduct):
    def generate(self) -> Dict[str, Any]:
        keyword = random.choice(["IBAN", "SWIFT"])
        return {
            "log_level": random.choice(LOG_LEVELS),
            "log_id": str(uuid.uuid4()),
            "type": "Transaction",
            "payload": f"Fund transfer via {keyword}. Initiator: {_generate_email()} | ID: {_generate_tckn()} | Source: {_generate_cc()}"
        }

class SystemErrorLog(LogProduct):
    def generate(self) -> Dict[str, Any]:
        return {
            "log_level": random.choice(LOG_LEVELS),
            "log_id": str(uuid.uuid4()),
            "type": "SystemError",
            "payload": f"Database timeout ERROR. Admin alert sent to {_generate_email()}. Last failed query referenced TCKN {_generate_tckn()} and Card {_generate_cc()}"
        }

class AccessLog(LogProduct):
    def generate(self) -> Dict[str, Any]:
        return {
            "log_level": random.choice(LOG_LEVELS),
            "log_id": str(uuid.uuid4()),
            "type": "Access",
            "payload": f"Unauthorized access attempt. Account: {_generate_email()}. Profile data accessed: TCKN {_generate_tckn()}, Saved Card {_generate_cc()}"
        }

class LogFactory:
    """Factory Method implementation for Log generation"""
    _creators = {
        "Transaction": TransactionLog,
        "SystemError": SystemErrorLog,
        "Access": AccessLog
    }

    @classmethod
    def create_log(cls, log_type: str) -> Dict[str, Any]:
        creator_class = cls._creators.get(log_type)
        if not creator_class:
            raise ValueError(f"Bilinmeyen log tipi: {log_type}")
        
        return creator_class().generate()