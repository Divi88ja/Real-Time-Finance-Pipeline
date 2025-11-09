from kafka import KafkaProducer
import requests, json, time, random

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Finnhub configuration
API_KEY = "d472ci1r01qh8nnapkfgd472ci1r01qh8nnapkg0"  # your API key
SYMBOL = "AAPL"  # Apple stock symbol

print("🚀 Kafka Producer started. Sending live data...")

while True:
    try:
        # Fetch real-time stock data
        response = requests.get(
            f'https://finnhub.io/api/v1/quote?symbol={SYMBOL}&token={API_KEY}'
        )
        data = response.json()

        # ✅ Add a proper, unique timestamp
        data["t"] = int(time.time())

        # ✅ Add small random variation to simulate real-time price movement
        if "c" in data and data["c"]:
            data["c"] = round(data["c"] + random.uniform(-0.5, 0.5), 4)
        if "h" in data and data["h"]:
            data["h"] = round(data["h"] + random.uniform(-0.3, 0.3), 4)
        if "l" in data and data["l"]:
            data["l"] = round(data["l"] + random.uniform(-0.3, 0.3), 4)
        if "o" in data and data["o"]:
            data["o"] = round(data["o"] + random.uniform(-0.4, 0.4), 4)

        # ✅ Send data to Kafka topic
        producer.send('finance_topic', data)
        print("📤 Sent:", data)

        # Wait 5 seconds before sending the next message
        time.sleep(5)

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(5)
