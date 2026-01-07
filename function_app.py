import azure.functions as func
import logging
import requests
import pyodbc
import os
from datetime import datetime

app = func.FunctionApp()

@app.schedule(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
def iRailFetcher(myTimer: func.TimerRequest) -> None:
    logging.info('Функция iRailFetcher запущена.')

    # 1. Берем строку подключения из настроек (мы добавим её в local.settings.json через минуту)
    connection_string = os.environ.get("SqlConnectionString")
    
    station = "Leuven"
    url = f"https://api.irail.be/liveboard/?station={station}&format=json&lang=en"

    try:
        # 2. Получаем данные
        response = requests.get(url)
        data = response.json()
        departures = data.get('departures', {}).get('departure', [])
        
        # 3. Подключаемся к SQL и записываем
        if connection_string:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    for train in departures[:10]: # Запишем первые 10 для теста
                        cursor.execute("""
                            INSERT INTO TrainDepartures (Station, Vehicle, DepartureTime, Delay, Platform, Destination)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, 
                        station, 
                        train['vehicle'], 
                        datetime.fromtimestamp(int(train['time'])), 
                        int(train['delay']) // 60, 
                        train['platform'], 
                        train['station'])
            logging.info(f"Successfully saved 10 trains in database!")
        else:
            logging.error("Строка подключения SqlConnectionString не найдена!")

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}")