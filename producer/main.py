import os
import time
import random
import requests
from factory import LogFactory

# Ortam değişkenleri üzerinden konfigürasyon
MIDDLEWARE_API_URL = os.environ.get("MIDDLEWARE_URL", "http://127.0.0.1:5000/api/logs")
STRESS_MODE = os.environ.get("STRESS_MODE", "True").lower() in ("true", "1", "t")

try:
    LOG_COUNT = int(os.environ.get("LOG_COUNT", "0"))
except ValueError:
    LOG_COUNT = 0

LOG_TYPES = ["Transaction", "SystemError", "Access"]

def main():
    print(f"Producer başlatıldı. Hedef: {MIDDLEWARE_API_URL}")
    print(f"Stres Modu: {'AÇIK' if STRESS_MODE else 'KAPALI'}")
    if STRESS_MODE and LOG_COUNT > 0:
        print(f"Hedeflenen Log Sayısı: {LOG_COUNT}")
    print("Loglar üretiliyor... Çıkış için CTRL+C")
    
    sent_count = 0
    start_time = time.time()  # Ölçüm başlangıcı
    
    with requests.Session() as session:
        while True:
            # Stres modunda belirli bir log sayısına ulaşıldıysa durdur
            if STRESS_MODE and LOG_COUNT > 0 and sent_count >= LOG_COUNT:
                end_time = time.time()
                elapsed = end_time - start_time
                rps = LOG_COUNT / elapsed if elapsed > 0 else 0
                
                print(f"\n[BİLGİ] Hedeflenen {LOG_COUNT} adet log gönderimi tamamlandı.")
                print(f"[PERFORMANS] Toplam Süre: {elapsed:.2f} saniye")
                print(f"[PERFORMANS] İşlem Hızı (Throughput): {rps:.2f} log/saniye")
                break

            log_type = random.choice(LOG_TYPES)
            log_data = LogFactory.create_log(log_type)
            
            try:
                response = session.post(MIDDLEWARE_API_URL, json=log_data, timeout=5)
                status = response.status_code
                print(f"[{status}] Gönderildi -> Tip: {log_type:<14} | Seviye: {log_data['log_level']} | Toplam: {sent_count + 1}")
            except requests.exceptions.RequestException as e:
                print(f"[BAĞLANTI HATASI] Middleware'e ulaşılamadı: {e}")
            
            sent_count += 1
            
            # Stres modu kapalıysa normal bekleme süresini işlet
            if not STRESS_MODE:
                time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProducer durduruldu.")