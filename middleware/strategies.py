import json
import csv
import os
from abc import ABC, abstractmethod
from typing import Dict, Any

class LogStrategy(ABC):
    @abstractmethod
    def write_log(self, log_data: Dict[str, Any]) -> None:
        pass

class HTMLStrategy(LogStrategy):
    def write_log(self, log_data: Dict[str, Any]) -> None:
        file_path = "sysadmin_logs.html"
        try:
            file_exists = os.path.exists(file_path)
            
            with open(file_path, "a", encoding="utf-8") as f:
                if not file_exists:
                    f.write("<!DOCTYPE html>\n<html>\n<head><title>System Admin Logs</title></head>\n<body>\n")
                    f.write("<table border='1'>\n<tr><th>Time</th><th>Server</th><th>ID</th><th>Level</th><th>Type</th><th>Payload</th></tr>\n")
                
                f.write(f"<tr>"
                        f"<td>{log_data.get('islenen_zaman', '')}</td>"
                        f"<td>{log_data.get('islem_sunucusu', '')}</td>"
                        f"<td>{log_data.get('log_id', '')}</td>"
                        f"<td>{log_data.get('log_level', '')}</td>"
                        f"<td>{log_data.get('type', '')}</td>"
                        f"<td>{log_data.get('payload', '')}</td>"
                        f"</tr>\n")
        except Exception as e:
            print(f"[HATA] HTML dosyasına yazılamadı: {e}")

class CSVStrategy(LogStrategy):
    def write_log(self, log_data: Dict[str, Any]) -> None:
        file_path = "cybersec_logs.csv"
        try:
            file_exists = os.path.exists(file_path)
            
            with open(file_path, "a", encoding="utf-8", newline="") as f:
                fieldnames = ["islenen_zaman", "islem_sunucusu", "log_id", "log_level", "type", "payload"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                row = {field: log_data.get(field, "") for field in fieldnames}
                writer.writerow(row)
        except Exception as e:
            print(f"[HATA] CSV dosyasına yazılamadı: {e}")

class JSONStrategy(LogStrategy):
    def write_log(self, log_data: Dict[str, Any]) -> None:
        file_path = "webdev_logs.json"
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                json.dump(log_data, f, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            print(f"[HATA] JSON dosyasına yazılamadı: {e}")

class StrategyContext:
    def __init__(self):
        self._strategies = {
            "SystemError": HTMLStrategy(),
            "Access": CSVStrategy(),
            "Transaction": JSONStrategy()
        }

    def execute_strategy(self, log_data: Dict[str, Any]) -> None:
        log_type = log_data.get("type")
        strategy = self._strategies.get(log_type)
        if strategy:
            strategy.write_log(log_data)
        else:
            print(f"[UYARI] Bilinmeyen Strateji: '{log_type}' tipi için bir strateji bulunamadı.")