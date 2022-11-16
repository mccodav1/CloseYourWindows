import requests, json, time, math
from datetime import datetime

temp_to_close_f = 74
temp_to_open_f = 72

close_windows = (temp_to_close_f - 32) * 5 / 9
open_windows = (temp_to_open_f - 32) * 5 / 9

windows_closed = False

delay = 60

api_key = "INSERT-KEY-HERE"

base_url = "http://api.openweathermap.org/data/2.5/weather?"

city_name = "Hochspeyer"

complete_url = base_url + "appid=" + api_key + "&q=" + city_name

response = requests.get(complete_url)

x = response.json()

temps_list = []
if x["cod"] != "404":
    time.sleep(1)
    while True:
        response = requests.get(complete_url)
        x = response.json()
        y = x["main"]
        current_temperature_k = y["temp"]
        current_temperature_c = current_temperature_k-273.15
        temps_list.append(current_temperature_c)
        temp_avg = sum(temps_list) / len(temps_list)
        status = "open" if not windows_closed else "closed"

        if len(temps_list) > 5:
            del temps_list[0]
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("\nCurrent Time =", current_time)
        print(f"Current temp is {round(current_temperature_c, 2)}. "
              f"\tAverage temp is {round(temp_avg, 2)}"
              f"\tWindows should be {status}.")
        if windows_closed:
            if temp_avg < open_windows:
                print("Time to open windows!")
                windows_closed = False
        else:
            if temp_avg > close_windows:
                print("Time to close windows!")
                windows_closed = True
        time.sleep(delay)

else:
    print('no')
