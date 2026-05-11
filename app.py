from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
print(f"Current Working Directory: {os.getcwd()}")
print(f".env file exists here: {os.path.exists('.env')}")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    cities_found = None
    weather_data = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        api_key = os.getenv("API_KEY")

        # CORRECT URL: Note the "/geo/1.0/direct?q=" bridge
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
        response = requests.get(geo_url)
        
        if response.status_code == 200:
            geo_response = response.json()
            
            if len(geo_response) > 1:
                cities_found = geo_response
            elif len(geo_response) == 1:
                # CORRECT URL: Note the "/data/2.5/weather?lat=" bridge
                lat = geo_response[0]['lat']
                lon = geo_response[0]['lon']
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
                
                res = requests.get(weather_url).json()
                weather_data = {
                    'city': res.get('name'),
                    'temp': res['main']['temp'],
                    'description': res['weather'][0]['description'],
                    'icon': res['weather'][0]['icon']
                }
            else:
                print("No city found.")
        else:
            print(f"Error from OpenWeather: {response.status_code}")

    return render_template('index.html', cities=cities_found, weather=weather_data)

@app.route('/weather')

def get_weather_by_coords():
    # This grabs the lat and lon from the URL you clicked
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    api_key = os.getenv("API_KEY")
    
    # The fixed weather URL
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    
    response = requests.get(url).json()
    
    # Format the data exactly like your index function does
    weather_data = {
        'city': response.get('name'),
        'temp': response['main']['temp'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }
    
    # Send it back to the same index.html page
    return render_template('index.html', weather=weather_data)

    


if __name__ == '__main__':
    app.run(debug=True)
