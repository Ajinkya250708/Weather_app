import tkinter as tk
import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings()


def get_weather_condition(code):

    if code == 0:
        return "☀️ Clear Sky"
    elif code in [1, 2]:
        return "🌤️ Partly Cloudy"
    elif code == 3:
        return "☁️ Cloudy"
    elif code in [51, 53, 55, 56, 57]:
        return "🌦️ Drizzle"
    elif code in [61, 63, 65, 66, 67]:
        return "🌧️ Rain"
    elif code in [71, 73, 75, 77]:
        return "❄️ Snow"
    elif code in [80, 81, 82]:
        return "🌧️ Rain Showers"
    elif code in [85, 86]:
        return "🌨️ Snow Showers"
    elif code in [95, 96, 99]:
        return "⛈️ Thunderstorm"
    else:
        return "🌥️ Unknown"


def clear_entry(event):

    if city_entry.get() == "Enter city name":
        city_entry.delete(0, tk.END)
        city_entry.config(fg="white")


def get_weather():

    city = city_entry.get()

    if city == "" or city == "Enter city name":
        weather_label.config(text="⚠️ Please enter a city name")
        return

    try:

        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

        response = requests.get(url, verify=False)
        data = response.json()

        if "results" not in data:
            weather_label.config(text="❌ City not found")
            return

        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]

        city_name = data["results"][0]["name"]
        country = data["results"][0]["country"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            f"&daily=temperature_2m_max,weather_code"
            f"&forecast_days=5"
            f"&timezone=auto"
        )

        weather_response = requests.get(weather_url, verify=False)
        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]

        condition = get_weather_condition(weather_code)

        daily = weather_data["daily"]

        dates = daily["time"]
        max_temps = daily["temperature_2m_max"]
        weather_codes = daily["weather_code"]

        forecast_text = "\n\n───────────────\n\n"
        forecast_text += "5 DAY FORECAST\n\n"

        today = datetime.now().date()

        for i in range(5):

            forecast_date = datetime.strptime(
                dates[i], "%Y-%m-%d"
            ).date()

            if forecast_date == today:
                day = "Today"
            elif forecast_date == today + timedelta(days=1):
                day = "Tomorrow"
            else:
                day = forecast_date.strftime("%a")

            emoji = get_weather_condition(
                weather_codes[i]
            ).split()[0]

            forecast_text += (
                f"{day:<10} {emoji}  {max_temps[i]}°C\n"
            )

        weather_label.config(
            text=f"📍 {city_name}, {country}\n\n"
                 f"{condition}\n\n"
                 f"🌡️ {temperature}°C\n"
                 f"💧 {humidity}%\n"
                 f"💨 {wind_speed} km/h"
                 f"{forecast_text}"
        )

    except Exception:

        weather_label.config(
            text="❌ Something went wrong!\nPlease try again."
        )


root = tk.Tk()

root.title("Weather App")
root.geometry("450x600")
root.resizable(False, False)
root.configure(bg="#121212")

title_label = tk.Label(
    root,
    text="🌦️ Weather App",
    font=("Arial", 30, "bold"),
    bg="#121212",
    fg="white"
)

title_label.pack(pady=(35, 5))

subtitle = tk.Label(
    root,
    text="Check current weather of any city",
    font=("Arial", 12),
    bg="#121212",
    fg="#aaaaaa"
)

subtitle.pack(pady=(0, 25))

city_entry = tk.Entry(
    root,
    font=("Arial", 16),
    width=25,
    justify="center",
    bg="#1e1e1e",
    fg="#888888",
    insertbackground="white",
    relief="flat"
)

city_entry.pack(ipady=10, pady=5)

city_entry.insert(0, "Enter city name")

city_entry.bind("<FocusIn>", clear_entry)

search_button = tk.Button(
    root,
    text="🔍  Get Weather",
    font=("Arial", 14, "bold"),
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=get_weather
)

search_button.pack(
    ipadx=20,
    ipady=8,
    pady=20
)

weather_frame = tk.Frame(
    root,
    bg="#1e1e1e",
    padx=35,
    pady=30,
    highlightbackground="#333333",
    highlightthickness=1
)

weather_frame.pack(
    padx=35,
    pady=15,
    fill="both"
)

weather_label = tk.Label(
    weather_frame,
    text="Enter a city\n\nto see the weather",
    font=("Arial", 15),
    justify="center",
    bg="#1e1e1e",
    fg="white",
    anchor="center"
)

weather_label.pack()

root.bind(
    "<Return>",
    lambda event: get_weather()
)

root.mainloop()