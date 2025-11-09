import psycopg2
from kafka import KafkaConsumer
import json
from src.utils.logger import get_logger
import yaml

# -----------------------------
# Connect to PostgreSQL
# -----------------------------
conn = psycopg2.connect(
    dbname="finance_stream_db",
    user="postgres",
    password="divija-postgre",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
print("✅ Connected to PostgreSQL successfully!")

# -----------------------------
# Load config and set up Kafka consumer
# -----------------------------
logger = get_logger("consumer")

with open("src/config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

TOPIC = cfg["kafka"]["topic"]
BROKER = cfg["kafka"]["broker"]

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# -----------------------------
# Create table if not exists
# -----------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data (
        c FLOAT,
        d FLOAT,
        dp FLOAT,
        h FLOAT,
        l FLOAT,
        o FLOAT,
        pc FLOAT,
        t BIGINT
    )
""")
conn.commit()

# -----------------------------
# Consume and insert messages
# -----------------------------
for msg in consumer:
    data = msg.value
    logger.info(f"Consumed: {data}")
    print("💾 Inserting into DB:", data)

    cursor.execute("""
        INSERT INTO market_data (c, d, dp, h, l, o, pc, t)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("c"),
        data.get("d"),
        data.get("dp"),
        data.get("h"),
        data.get("l"),
        data.get("o"),
        data.get("pc"),
        data.get("t")
    ))
    conn.commit()
