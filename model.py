import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from geopy.geocoders import Nominatim


def geocode(location):
    
    API_KEY = "6InE6yDIkM9s9ycSCiS9U9VqzuAUibXM8FfVVGVoGmM"  
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={location}&apiKey={API_KEY}"
    print(url)
    response = requests.get(url)
    data = response.json()
    
    result = data['items'][0]
    lat = result['position']['lat']
    lng = result['position']['lng']
    return lat, lng



# Define the API key 
API_KEY = "2a84c4a7c3b340a8a4145545240609"

# Function to get environmental data for the given latitude and longitude
def get_earth_data(latitude, longitude):
    # OpenWeatherMap endpoint for one call API (provides environmental data)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={latitude},{longitude}&days=1&aqi=no&alerts=no"
    
    print(url)
    # Send the request
    response = requests.get(url)

    # Check if the request was successful
    
    data = response.json()
        # Extract relevant information (e.g., current weather, precipitation, etc.)
    current_weather = data['current']
    precipitation = current_weather.get('rain', {}).get('1h', 0)  # precipitation in last 1 hour (if available)
    return  precipitation
    
   
    



csv_file= 'C:/Users/ASUS/Desktop/hack/modified_data.csv'
def get_population_data(location, csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)
    
    # Assuming the city names are in the 1st column and population in the 4th column
    city_column = data.columns[0]  # Update if your city column has a different index or name
    population_column = data.columns[3]  # Population is in the 4th column (index 3)
    
    # Create a dictionary from the CSV
    population_data = dict(zip(data[city_column], data[population_column]))
    
    # Return the population for the specified location, defaulting to 1,000,000 if not found
    return population_data.get(location, 1000000)



def get_water_availability(location, csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)
    
    # Assuming the city names are in the 1st column and population in the 4th column
    city_column = data.columns[0]  # Update if your city column has a different index or name
    availability_column = data.columns[2]  
    
    # Create a dictionary from the CSV
    availability_data = dict(zip(data[city_column], data[availability_column]))
    
    # Return the availability for the specified location, defaulting to 1,000 if not found
    return availability_data.get(location, 1000)

def get_water_usage(location, csv_file):
    data = pd.read_csv(csv_file)
    city_column = data.columns[0]  # Assuming cities are in the 1st column
    usage_column = data.columns[1]  # Assuming water usage is in the 2nd column
    usage_data = dict(zip(data[city_column], data[usage_column]))
    return usage_data.get(location, 100)



def get_features(location, csv_file):
        latitude, longitude = geocode(location)
        
        population = get_population_data(location, csv_file)
        water_availability = get_water_availability(location, csv_file)
        rain = get_earth_data(latitude, longitude)
        
        return [population, water_availability, rain]




def predict_water_usage(location,csv_file):
    locations=['Tunisia' ,'congo' ,'Central African Republic', 'Benin',

'maldives' ,'Rwanda' ,'comoros' ,'uganda' ,'Lesotho' ,'equatorial' ,'guinea', 'Djibouti' ,'togo' ,'angola' ,'sierra leone ',

'Burundi' ,'liberia' , 'Côte d\'Ivoire' ,'cabo verde']
    # Create X based on population, water availability, and rain
    X = [get_features(loc, csv_file) for loc in locations]
    y = [get_water_usage(loc, csv_file) for loc in locations]
    model = RandomForestRegressor(n_estimators=10)
    model.fit(X, y)
    input_data = [get_features(location,csv_file)]
    predicted_usage = model.predict(input_data)
    return predicted_usage[0]



# Main function to get user inputs and make predictions
def main():
    location = input("Enter the location/region: ")
    
    # Step 5: Predict daily water usage per person
    predicted_water_usage = predict_water_usage(location,csv_file)
    print(f"Predicted daily water usage per person: {predicted_water_usage:.2f} liters")

if __name__ == "__main__":
    main()