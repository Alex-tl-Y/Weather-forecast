import tkinter as tk
import requests
from PIL import Image, ImageTk
from datetime import datetime

def setup_forecast(event): 
    user_input = cityEntry.get()

    coords = get_coords(user_input)

    for frame in [forecastFrame, feelsLikeFrame, humidityFrame, precipitationFrame, visibilityFrame, windFrame]:
        for widget in frame.winfo_children():
            widget.destroy()

    # Unable to find the location
    if coords == None: 
       
        invalidLabel = tk.Label(forecastFrame, text = "Please enter a valid city.")
        invalidLabel.pack()

    # Location has been found
    else: 

        data = get_weather(coords[0], coords[1])

        # Important weather information
        weatherCode = data["current"]["weather_code"]
        windDegrees = data["current"]["wind_direction_10m"]
        temperature = data["current"]["temperature_2m"]
        wind_speed = data["current"]["wind_speed_10m"]
        feelsLike = data["current"]["apparent_temperature"]
        humidity = data["current"]["relative_humidity_2m"]
        precipitation = data["current"]["precipitation"]
        visibility = data["current"]["visibility"]

        # Classifies the weather code
        if (weatherCode == 0):
            img = ImageTk.PhotoImage(sunny)
            imgLabel = "Clear Sky"
        elif(weatherCode == 1):
            img = ImageTk.PhotoImage(sunny)
            imgLabel = "Mainly Clear"
        elif(weatherCode == 2):
            img = None
            imgLabel = "Party Cloudy"
        elif(weatherCode == 3):
            img = None
            imgLabel = "Cloudy"
        elif(weatherCode == 45 or weatherCode == 48):
            img = None
            imgLabel = "Foggy"
        elif(weatherCode == 51 or weatherCode == 53 or weatherCode == 55):
            img = None
            imgLabel = "Drizzle"
        elif (weatherCode == 61 or weatherCode == 63 or weatherCode == 65):
            img = ImageTk.PhotoImage(rainy)
            imgLabel = "Rainy"
        elif(weatherCode == 66 or weatherCode == 67):
            img = None
            imgLabel = "Freezing Rain"
        elif(weatherCode == 71 or weatherCode == 73 or weatherCode == 75):
            img = ImageTk.PhotoImage(snowing)
            imgLabel = "Snowing"
        elif(weatherCode == 77):
            img = None
            imgLabel = "Snow grains"
        elif (weatherCode == 80 or weatherCode == 81 or weatherCode == 82): 
            img = None
            imgLabel = "Rain Showers"
        elif(weatherCode == 85 or weatherCode == 86):
            img = None
            imgLabel = "Snow Showers"
        elif (weatherCode == 95 or weatherCode == 96 or weatherCode == 99):
            img = ImageTk.PhotoImage(thunder)
            imgLabel = "Thunderstorms"

        # Classifies the wind direction
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(windDegrees / 45) % 8
        wind_direction = directions[index]

        canvas1 = tk.Canvas(forecastFrame, bg = 'darkblue', width = 100, height = 100, highlightthickness=0, bd = 0)
        canvas1.place(relx=0.4, rely = 0.25)
        canvas1.create_image(50, 50, image = img)
        canvas1.img = img
        
        currentLabel = tk.Label(forecastFrame, text = "Current Weather", bg = forecastFrame["bg"], fg = "white", font = ("Times New Roman", 25, "bold"))
        currentTime = tk.Label(forecastFrame, text = datetime.now().strftime("%I:%M %p"), bg =forecastFrame["bg"], fg = "white", font = ("Times New Roman", 15))
        weatherLabel = tk.Label(forecastFrame, text = imgLabel, bg = forecastFrame["bg"], fg = "white", font = ("Times New Roman", 15))
        tempLabel = tk.Label(forecastFrame, text = str(temperature) + "°C", bg = forecastFrame["bg"], fg = "white", font = ("Times New Roman", 30, "bold"))
        currentLabel.place(relx = 0, rely = 0.05)
        currentTime.place(relx = 0, rely = 0.2)
        weatherLabel.place(relx = 0.6, rely = 0.2)
        tempLabel.place(relx = 0.6, rely= 0.35)

        feelsLikeTitle = tk.Label(feelsLikeFrame, text = "Feels Like", font = ("Times New Roman", 20), bg = feelsLikeFrame["bg"])
        feelsLikeLabel = tk.Label(feelsLikeFrame, text = str(feelsLike) + "°C", bg = feelsLikeFrame["bg"], font = ("Times New Roman", 15))
        feelsLikeTitle.place(relx = 0.5, rely = 0.1, anchor = "center")
        feelsLikeLabel.place(relx = 0.5, rely = 0.3)

        humidityTitle = tk.Label(humidityFrame, text = "Humidity", font = ("Times New Roman", 20), bg = humidityFrame["bg"])
        humidityLabel = tk.Label(humidityFrame, text = str(humidity) + "%", bg = humidityFrame["bg"], font = ("Times New Roman", 15))
        humidityTitle.place(relx = 0.5, rely = 0.1, anchor = "center")
        humidityLabel.place(relx = 0.5, rely = 0.3)

        visibilityTitle = tk.Label(visibilityFrame, text = "Visibility Levels", font = ("Times New Roman", 20), bg = visibilityFrame["bg"])
        visibilityLabel = tk.Label(visibilityFrame, text = str(visibility) + "m", bg = visibilityFrame["bg"], font = ("Times New Roman", 15))
        visibilityTitle.place(relx = 0.5, rely = 0.1, anchor = "center")
        visibilityLabel.place(relx=0.5, rely=0.3)

        precipitationTitle = tk.Label(precipitationFrame, text = "Precipition", font = ("Times New Roman", 20), bg = precipitationFrame["bg"])
        precipitationLabel = tk.Label(precipitationFrame, text = str(precipitation) + "mm", bg = precipitationFrame["bg"], font = ("Times New Roman", 15))
        precipitationTitle.place(relx = 0.5, rely = 0.1, anchor = "center")
        precipitationLabel.place(relx = 0.5, rely = 0.3)
        
        windTitle = tk.Label(windFrame, text = "Wind", font = ("Times New Roman", 20), bg = windFrame["bg"])
        windspeedLabel = tk.Label(windFrame, text = wind_direction + " " + str(wind_speed) + "km/h", bg = windFrame["bg"], font = ("Times New Roman", 15))
        windTitle.place(relx = 0.5, rely = 0.1, anchor = "center")
        windspeedLabel.place(relx = 0.5, rely = 0.3)      
       
# API call to get weather data
def get_weather(long: str, lat: str):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,visibility,relative_humidity_2m,is_day,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,wind_speed_10m,wind_direction_10m,is_day&timezone=America%2FNew_York"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data
    else: 
        return None

# API call to get the longtitude and latitude of a city
def get_coords(city: str):
    url =  f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"

    response = requests.get(url)

    if (response.status_code == 200 and "results" in response.json()): 
        data = response.json()

        long = data["results"][0]["longitude"]
        lat = data["results"][0]["latitude"]

        return (long, lat)
    else:
        return None
    
if __name__ == "__main__":

    # All the images
    sunny = Image.open("images/sunny.png").convert("RGBA")
    sunny = sunny.resize((100, 100))

    cloudy = Image.open("images/cloudy.png")
    cloudy = cloudy.resize((100, 100))

    rainy = Image.open("images/rainy.png")
    rainy = rainy.resize((100, 100))

    thunder = Image.open("images/thunder.png")
    thunder = thunder.resize((100, 100))

    snowing = Image.open("images/snowing.png")
    snowing = snowing.resize((100, 100))

    wind = Image.open("images/wind.png")

    daytime = Image.open("images/daytime.jpg")

    nighttime = Image.open("images/nighttime.jpg")

    search_icon = Image.open("images/search_icon.png")
    search_icon = search_icon.resize((48, 48))

    # Creating the application GUI
    root = tk.Tk()
    root.title("Weather App")
    root.geometry("1150x800")

    # Setting up background 
    bg_image = ImageTk.PhotoImage(daytime)
    bg_label = tk.Label(root, image = bg_image)
    bg_label.pack()
    bg_label.image = bg_image

    # Setting up the search entry
    cityEntry = tk.Entry(root, font = ("Times New Roman", 30))
    cityEntry.place(x = 25, y = 200, width = 400, height = 50)
    cityEntry.bind('<Return>', setup_forecast)

    search_image = ImageTk.PhotoImage(search_icon)
    search_label = tk.Label(root, image = search_image)
    search_label.place(x = 430, y = 200)
    search_label.image = search_image


    # Setting up the forecast frame
    forecastFrame = tk.Frame(root, bg = 'darkblue', highlightbackground="blue", highlightthickness=2)
    forecastFrame.place(x = 500, y = 25, width = 635, height = 350)

    extraInfoFrame = tk.Frame(root, bg = "white")
    extraInfoFrame.place(x = 10, y = 425, width = 1125, height = 370)
    
    feelsLikeFrame = tk.Frame(root, bg = 'lightgray')
    feelsLikeFrame.place(x = 25, y = 450, width = 200, height = 300)

    humidityFrame = tk.Frame(root, bg = 'lightgray')
    humidityFrame.place(x = 250, y = 450, width = 200, height = 300)

    visibilityFrame = tk.Frame(root, bg = 'lightgray')
    visibilityFrame.place(x = 475, y = 450, width = 200, height = 300)

    precipitationFrame = tk.Frame(root, bg = 'lightgray')
    precipitationFrame.place(x = 700, y = 450, width = 200, height = 300)

    windFrame = tk.Frame(root, bg = 'lightgray')
    windFrame.place(x = 925, y = 450, width = 200, height = 300)

    root.mainloop()