from dotenv import load_dotenv
import os
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, Float, String, DateTime, Boolean
)


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost") 
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
SHELLY_IP = os.getenv("SHELLY_IP")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
metadata = MetaData()

# ⚡ 1. Мгновенные показатели по фазам
power_instant_log = Table("power_instant_log", metadata,
    Column("timestamp", DateTime, primary_key=True),
    Column("a_voltage", Float), Column("a_current", Float), Column("a_act_power", Float), Column("a_aprt_power", Float), Column("a_pf", Float), Column("a_freq", Float),
    Column("b_voltage", Float), Column("b_current", Float), Column("b_act_power", Float), Column("b_aprt_power", Float), Column("b_pf", Float), Column("b_freq", Float),
    Column("c_voltage", Float), Column("c_current", Float), Column("c_act_power", Float), Column("c_aprt_power", Float), Column("c_pf", Float), Column("c_freq", Float),
    Column("total_current", Float), Column("total_act_power", Float), Column("total_aprt_power", Float)
)

# 🔋 2. Накопленные значения энергии
energy_accumulated_log = Table("energy_accumulated_log", metadata,
    Column("timestamp", DateTime, primary_key=True),
    Column("a_total_act_energy", Float), Column("a_total_act_ret_energy", Float),
    Column("b_total_act_energy", Float), Column("b_total_act_ret_energy", Float),
    Column("c_total_act_energy", Float), Column("c_total_act_ret_energy", Float),
    Column("total_act", Float), Column("total_act_ret", Float)
)

# 🌡 3. Температура устройства
temperature_log = Table("temperature_log", metadata,
    Column("timestamp", DateTime, primary_key=True),
    Column("tC", Float),
    Column("tF", Float)
)

# ⚙ 4. Статус системы (uptime, память, файловая система)
device_status_log = Table("device_status_log", metadata,
    Column("timestamp", DateTime, primary_key=True),
    Column("uptime", Integer),
    Column("ram_size", Integer),
    Column("ram_free", Integer),
    Column("ram_min_free", Integer),
    Column("fs_size", Integer),
    Column("fs_free", Integer),
    Column("restart_required", Boolean),
    Column("reset_reason", Integer)
)

# 📶 5. Статус WiFi
wifi_status_log = Table("wifi_status_log", metadata,
    Column("timestamp", DateTime, primary_key=True),
    Column("sta_ip", String),
    Column("ssid", String),
    Column("status", String),
    Column("rssi", Integer)
)

# Создание всех таблиц в БД
metadata.create_all(engine)

print("[✅] База данных и таблицы успешно созданы!")


