from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests





url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'


config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']





def search():
    city = city_text.get()
    weather = getWeather(city)
    if weather:
        location_lbl["text"] = '{}, {}'.format(weather[0], weather[1])
        temp_label["text"] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_label["text"] = weather[4]

    else:
        messagebox.showerror('Error', 'Cannot find the city name{}'.format(city))


def getWeather(city):
    result = requests.get(url.format(city,api_key))
    if result:
        json = result.json()
        # (City, Country, temp_in_fahrenheit, temp_in_celsius, icon,  weather)
        city = json["name"]
        country = json["sys"]["country"]
        temp_kelvin = json["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
        weather = json["weather"][0]["main"]
        final = (city, country, temp_celsius, temp_fahrenheit, weather)

        return final


    else:
        return None

print(getWeather('London'))


app = Tk()
app.title("Weather App by Ak")
app.geometry('360x480')


city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text='Search weather', width=12, command=search)
search_btn.pack()

location_lbl = Label(app, text='', font=('bold', 20))
location_lbl.pack()

image = Label(app, bitmap='')
image.pack()


temp_label = Label(app, text='')
temp_label.pack()


weather_label = Label(app, text='')
weather_label.pack()







app.mainloop()
