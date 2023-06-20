import tensorflow as tf
import requests
import json
import numpy as np
# Set your Thingspeak API key and channel ID
API_KEY = 'N2FJP53Q2OIEDX4M'
CHANNEL_ID = '1958878'

# Set the URL for the Thingspeak API
URL = 'https://api.thingspeak.com/channels/{}/feeds.json?api_key={}'.format(CHANNEL_ID, API_KEY)

# Set the URL for the Open Weather API
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?lat=13&lon=77.5&appid=406b154331868aa69ddc3dd64454c8c6'

# Load the model
model = tf.keras.models.load_model('C:\\Users\\Asus\\Desktop\\my_model.h5')

def read_data_from_thingspeak_and_open_weather():
    # Read the latest entry from Thingspeak
    response = requests.get(URL)
    data = response.json()
    latest_entry = data['feeds'][-1]
    vsm = int(latest_entry['field3'])*.72/100
   # print(vsm)
    # Read the current weather from the Open Weather API
    weather_response = requests.get(WEATHER_URL)
    weather_data = weather_response.json()
    weather = weather_data['weather'][0]['main']
    #print(weather_data['main']['temp'])
    #print([latest_entry['field3'], latest_entry['field2'], weather])
    # Return the data as a NumPy array
    return [weather_data['main']['temp']-273, 0, vsm]

def write_prediction_to_thingspeak(prediction):
    # Format the prediction as a string
    prediction_str = 'field1={}'.format(prediction)

    # Send the prediction to Thingspeak
    requests.post(URL, data={'field3': prediction[0][0][0]})

# Read data from Thingspeak and the Open Weather API
data = read_data_from_thingspeak_and_open_weather()

# Use the model to make a prediction
prediction = model.predict([[data]])
API_KEY = 'ZHOH25HNVZC2KLJM'
CHANNEL_ID = '1978647'

# Set the URL for the Thingspeak API
URL = 'https://api.thingspeak.com/channels/{}/feeds.json?api_key={}'.format(CHANNEL_ID, API_KEY)
# Write the prediction to Thingspeak
print(prediction[0])
write_prediction_to_thingspeak(prediction)