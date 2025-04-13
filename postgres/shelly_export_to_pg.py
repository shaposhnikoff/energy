import datetime
import requests
from sqlalchemy import (create_engine, insert, MetaData, Table)
from time import sleep

from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST") 
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
SHELLY_IP = os.getenv("SHELLY_IP")



engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

metadata = MetaData()
metadata.reflect(bind=engine)

power_table = metadata.tables["power_instant_log"]
energy_table = metadata.tables["energy_accumulated_log"]
temp_table = metadata.tables["temperature_log"]
status_table = metadata.tables["device_status_log"]
wifi_table = metadata.tables["wifi_status_log"]




while True:
    sleep(60)
    # выводи время запуска 
    
    print(f"Время запуска: {datetime.datetime.now()}")
    try:
        response = requests.get(f"http://{SHELLY_IP}/rpc/Shelly.GetStatus", timeout=3)
        status = response.json()
        now = datetime.datetime.now()

        with engine.begin() as conn:
            # 💡 power_instant_log
            em = status.get("em:0", {})
            conn.execute(insert(power_table).values(
                timestamp=now,
                a_voltage=em.get("a_voltage"),
                a_current=em.get("a_current"),
                a_act_power=em.get("a_act_power"),
                a_aprt_power=em.get("a_aprt_power"),
                a_pf=em.get("a_pf"),
                a_freq=em.get("a_freq"),
                b_voltage=em.get("b_voltage"),
                b_current=em.get("b_current"),
                b_act_power=em.get("b_act_power"),
                b_aprt_power=em.get("b_aprt_power"),
                b_pf=em.get("b_pf"),
                b_freq=em.get("b_freq"),
                c_voltage=em.get("c_voltage"),
                c_current=em.get("c_current"),
                c_act_power=em.get("c_act_power"),
                c_aprt_power=em.get("c_aprt_power"),
                c_pf=em.get("c_pf"),
                c_freq=em.get("c_freq"),
                total_current=em.get("total_current"),
                total_act_power=em.get("total_act_power"),
                total_aprt_power=em.get("total_aprt_power")
            ))

            # 💡 energy_accumulated_log
            emdata = status.get("emdata:0", {})
            conn.execute(insert(energy_table).values(
                timestamp=now,
                a_total_act_energy=emdata.get("a_total_act_energy"),
                a_total_act_ret_energy=emdata.get("a_total_act_ret_energy"),
                b_total_act_energy=emdata.get("b_total_act_energy"),
                b_total_act_ret_energy=emdata.get("b_total_act_ret_energy"),
                c_total_act_energy=emdata.get("c_total_act_energy"),
                c_total_act_ret_energy=emdata.get("c_total_act_ret_energy"),
                total_act=emdata.get("total_act"),
                total_act_ret=emdata.get("total_act_ret")
            ))

            # 💡 temperature_log
            temp = status.get("temperature:0", {})
            conn.execute(insert(temp_table).values(
                timestamp=now,
                tC=temp.get("tC"),
                tF=temp.get("tF")
            ))

            # 💡 device_status_log
            sys = status.get("sys", {})
            conn.execute(insert(status_table).values(
                timestamp=now,
                uptime=sys.get("uptime"),
                ram_size=sys.get("ram_size"),
                ram_free=sys.get("ram_free"),
                ram_min_free=sys.get("ram_min_free"),
                fs_size=sys.get("fs_size"),
                fs_free=sys.get("fs_free"),
                restart_required=sys.get("restart_required"),
                reset_reason=sys.get("reset_reason")
            ))

            # 💡 wifi_status_log
            wifi = status.get("wifi", {})
            conn.execute(insert(wifi_table).values(
                timestamp=now,
                sta_ip=wifi.get("sta_ip"),
                ssid=wifi.get("ssid"),
                status=wifi.get("status"),
                rssi=wifi.get("rssi")
            ))

        print("[✅] Данные успешно собраны и записаны в БД.")

    except requests.exceptions.RequestException as e:
        print(f"[⚠️] Ошибка подключения к Shelly: {e}")
    except Exception as e:
        print(f"[❌] Ошибка при обработке данных: {e}")


