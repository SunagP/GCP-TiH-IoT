import tensorflow as tf
import requests
import json
import numpy as np
import time

# Set your Thingspeak API key and channel id
API_KEY = 'SO50RIFJSC1IIO7K'
CHANNEL_ID = '2028980'


# Set the URL for the Thingspeak API
URL = 'https://api.thingspeak.com/channels/{}/feeds.json?api_key={}'.format(CHANNEL_ID, API_KEY)

API_KEY = 'ZHOH25HNVZC2KLJM'
CHANNEL_ID = '1978647'

# Set the URL for the Thingspeak API
WURL = 'https://api.thingspeak.com/channels/{}/feeds.json?api_key={}'.format(CHANNEL_ID, API_KEY)
# Set the URL for the Open Weather API
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?lat=13&lon=77.5&appid=406b154331868aa69ddc3dd64454c8c6'

# Load the model
model = tf.keras.models.load_model('my_model.h5')

def read_data_from_thingspeak_and_open_weather():
    # Read the latest entry from Thingspeak
    response = requests.get(URL)
    data = response.json()
    latest_entry = data['feeds'][-1]
    vsm = int(latest_entry['field2'])*.72/100
  
    # Read the current weather from the Open Weather API
    weather_response = requests.get(WEATHER_URL)
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp']-273
    rain  = 0
    if "rain" in weather_data.keys():
        rain = weather_data["rain"]
    
    else:
        rain = 0
    # Return the data as a NumPy array
    requests.post(WURL, data={'field1': temperature})
    time.sleep(16)
    print("Done")
    requests.post(WURL, data={'field2': rain})
    time.sleep(16)
    print("Done")
    requests.post(WURL, data={'field4': vsm})
    time.sleep(16)
    print("Done")
    requests.post(WURL, data={'field5':150})
    return [temperature, rain, vsm]

def write_prediction_to_thingspeak(prediction):
    # Format the prediction as a string
    prediction_str = 'field1={}'.format(prediction)

    # Send the prediction to Thingspeak
    requests.post(WURL, data={'field3': prediction[0][0][0]})
    

# Read data from Thingspeak and the Open Weather API
data = read_data_from_thingspeak_and_open_weather()

# Use the model to make a prediction
prediction = model.predict([[data]])

# Write the prediction to Thingspeak
#print(prediction[0])
write_prediction_to_thingspeak(prediction)