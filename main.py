import python_weather
import asyncio
import os
import customtkinter as tk
import tkintermapview as tkmapview
import configparser

class WeatherApp:
    def __init__(self):
        self.load_config()
        self.ui()

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.cfg')

    def ui(self):
        self.home_pos = self.config.get('Main', 'home_pos')

        tk.set_appearance_mode("System")
        tk.set_default_color_theme("blue")

        self.app = tk.CTk()
        self.app.geometry("800x600")
        self.app.title("WeatherMaps")

        self.map_widget = tkmapview.TkinterMapView(self.app, width=800, height=600, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.map_widget.set_position(*map(float, self.home_pos.split(',')))
        self.map_widget.set_zoom(10)

        self.app.mainloop()

    async def fetch_weather(self):
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            self.weather = await client.get('Worcester')

            print(self.weather.temperature)

            for daily in self.weather.daily_forecasts:
                print(daily)

                for hourly in daily.hourly_forecasts:
                    print(f'{hourly!r}')

    def get_weather(self):
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(self.fetch_weather())

if __name__ == '__main__':
    WeatherApp()
