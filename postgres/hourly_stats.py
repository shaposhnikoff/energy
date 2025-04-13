import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST") 
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
SHELLY_IP = os.getenv("SHELLY_IP")


# Подключение к БД
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# SQL-запрос: берём последний total_act за каждый час
query = text("""
    SELECT
        date_trunc('hour', timestamp) AS hour,
        MAX(total_act) AS total_act
    FROM energy_accumulated_log
    WHERE timestamp >= NOW() - interval '2 days'
    GROUP BY hour
    ORDER BY hour
""")

with engine.connect() as conn:
    df = pd.read_sql(query, conn)

# Считаем разницу по total_act (Δ кВт⋅ч)
df['consumed_kwh'] = df['total_act'].diff() / 1000

# Красиво выводим
print("\n📊 Hourly Power Consumption:")
print(df[['hour', 'consumed_kwh']].fillna(0).round(3).to_string(index=False))

