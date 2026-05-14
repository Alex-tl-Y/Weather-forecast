import tkinter as tk
import requests
def setup_forecast(event): 
    user_input = cityEntry.get()

    coords = get_coords(user_input)

    for widget in forecastFrame.winfo_children():
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
            img = sunny
            imgLabel = "Clear Sky"
        elif(weatherCode == 1):
            img = sunny
            imgLabel = "Mainly Clear"
        elif(weatherCode == 2):
            img = None
            imgLabel = "Party Cloudy"
        elif(weatherCode == 3):
            img = None
            imgLabel = "Cloudy"
        elif(weatherCode == 45 or weatherCode == 48):
            img = fog
            imgLabel = "Foggy"
        elif(weatherCode == 51 or weatherCode == 53 or weatherCode == 55):
            img = sunny
            imgLabel = "Drizzle"
        elif (weatherCode == 61 or weatherCode == 63 or weatherCode == 65):
            img = rainy
            imgLabel = "Rainy"
        elif(weatherCode == 66 or weatherCode == 67):
            img = None
            imgLabel = "Freezing Rain"
        elif(weatherCode == 71 or weatherCode == 73 or weatherCode == 75):
            img = snowing
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
            img = thunder
            imgLabel = "Thunderstorms"

        # Classifies the wind direction
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(windDegrees / 45) % 8
        wind_direction = directions[index]

        weatherIcon = tk.Label(forecastFrame, image=img)
        weatherLabel = tk.Label(forecastFrame, text = imgLabel)
        tempLabel = tk.Label(forecastFrame, text = str(temperature))
        windspeedLabel = tk.Label(windFrame, text = str(wind_speed))
        windDirectionLabel = tk.Label(windFrame, text = wind_direction)
        feelsLikeLabel = tk.Label(feelsLikeFrame, text = str(feelsLike))
        humidityLabel = tk.Label(humidityFrame, text = str(humidity))
        precipitationLabel = tk.Label(precipitationFrame, text = str(precipitation))
        visibilityLabel = tk.Label(visibilityFrame, text = str(visibility))
        

        weatherIcon.pack()
        weatherLabel.pack()
        tempLabel.pack()
        windspeedLabel.pack()
        windDirectionLabel.pack()
        feelsLikeLabel.pack()
        humidityLabel.pack()
        precipitationLabel.pack()
        visibilityLabel.pack()            
       
# API call to get weather data
def get_weather(long: str, lat: str):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,visibility,relative_humidity_2m,is_day,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,wind_speed_10m,wind_direction_10m&timezone=America%2FNew_York"

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
    # Creating the application GUI
    root = tk.Tk()
    root.title("Weather App")
    root.geometry("800x800")

    # All the images
    sunny = tk.PhotoImage(file="images/sunny.png")
    cloudy = tk.PhotoImage(file="images/cloudy.png")
    rainy = tk.PhotoImage(file="images/rainy.png")
    thunder = tk.PhotoImage(file="images/thunder.png")
    snowing = tk.PhotoImage(file="images/snowing.png")
    wind = tk.PhotoImage(file="images/wind.png")

    # Setting up the search frame
    searchFrame = tk.Frame(root, bg = 'lightblue')
    searchFrame.place(x = 25, y = 25, width = 250, height = 100)
    cityEntry = tk.Entry(searchFrame)
    cityEntry.pack()
    cityEntry.bind('<Return>', setup_forecast)

    # Setting up the forecast frame
    forecastFrame = tk.Frame(root, bg = 'darkblue')
    forecastFrame.place(x = 300, y = 25, width = 450, height = 300)

    # Setting up the extra frame
    extraFrame = tk.Frame(root, bg = 'gray')
    extraFrame.place(x = 25, y = 400, width = 750, height = 400)
    feelsLikeFrame = tk.Frame(extraFrame, bg = 'blue')
    feelsLikeFrame.grid(row = 0, column = 0, sticky = 'news')
    humidityFrame = tk.Frame(extraFrame, bg = 'lightgray')
    humidityFrame.grid(row = 0, column=1)
    visibilityFrame = tk.Frame(extraFrame, bg = 'lightgray')
    visibilityFrame.grid(row=0, column=2)
    precipitationFrame = tk.Frame(extraFrame, bg = 'lightgray')
    precipitationFrame.grid(row=0, column = 3)
    windFrame = tk.Frame(extraFrame, bg = 'lightgray')
    windFrame.grid(row=0, column=4)




    enterLabel = tk.Label(searchFrame, text = "Enter city ")
    enterLabel.pack()


    root.mainloop()