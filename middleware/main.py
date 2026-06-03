import time
from flask import Flask, request, jsonify
from chain import PerformanceFilterHandler, SecurityMaskingHandler, EnrichmentHandler
from strategies import StrategyContext

app = Flask(__name__)

# Zincir Kurulumu
performance_handler = PerformanceFilterHandler()
security_handler = SecurityMaskingHandler()
enrichment_handler = EnrichmentHandler()

performance_handler.set_next(security_handler).set_next(enrichment_handler)

# Strateji Bağlamı
strategy_context = StrategyContext()

@app.route("/api/logs", methods=["POST"])
def receive_logs():
    start_time = time.time()  # İç gecikme ölçümü başlangıcı
    
    log_data = request.get_json(silent=True)
    if not log_data:
        return jsonify({"error": "Geçersiz payload"}), 400

    # Adım 1: Chain of Responsibility (Performans -> Güvenlik -> Zenginleştirme)
    processed_data = performance_handler.handle(log_data)

    # Performans filtresinden geçemediyse
    if processed_data.get("status") == "ignored":
        process_time_ms = (time.time() - start_time) * 1000
        print(f"[PERFORMANS - REDDEDİLDİ] İç Gecikme: {process_time_ms:.2f} ms")
        return jsonify({"status": "ignored", "reason": processed_data.get("reason")}), 200

    # Adım 2: Strateji Seçimi ve Dosyaya Yazma
    strategy_context.execute_strategy(processed_data)

    process_time_ms = (time.time() - start_time) * 1000
    print(f"[PERFORMANS - İŞLENDİ] İç Gecikme: {process_time_ms:.2f} ms | Tip: {processed_data.get('type')}")

    return jsonify({"status": "processed"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)