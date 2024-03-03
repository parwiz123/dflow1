from flask import Flask, request, jsonify
import requests

application  = Flask(__name__)
CORS(application)  # This will enable CORS for all routes

@application.route('/')
def hello():
    return "Hello World"



@application.route('/webhook', methods=['POST'])
def webhook():
    # Parse the incoming JSON request
    req = request.get_json(force=True)

    # Extracting the location parameter from the request
    location = req['queryResult']['parameters'].get('geo-city')

    # Check if location parameter is provided
    if not location:
        return jsonify({'fulfillmentText': "Please provide a location."})

    # OpenWeatherMap API key
    api_key = '9524bb51cf5f8675427d00260d806fbb'

    # Construct the URL for the API request
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    # Send a GET request to the OpenWeatherMap API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        return jsonify({'fulfillmentText': "Sorry, I couldn't retrieve the weather data at the moment."})

    # Parse the JSON response from the API
    weather_data = response.json()

    # Extract temperature and weather description from the response
    temperature = weather_data['main']['temp']
    weather_description = weather_data['weather'][0]['description']

    # Create a response message with the weather information
    fulfillment_text = f"The current temperature in {location} is {temperature}°C with {weather_description}."

    # Return the response to DialogFlow
    return jsonify({'fulfillmentText': fulfillment_text})

if __name__ == '__main__':
    application.run(debug=True)
