# weather_visualizer.py

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


API_KEY = "771d8e6d24d2228237f11af282e9eb6a" 
CITY_NAME = "iran" # You can change this to any city

def fetch_weather_data(api_key, city):
    """Fetches weather data from the OpenWeatherMap API for a given city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    # We add 'units=metric' to get temperature in Celsius
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric" 
    }
    
    print(f"Fetching weather data for {city}...")
    try:
        response = requests.get(base_url, params=params)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status() 
        print("Data fetched successfully!")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 401:
            print("Error: Invalid API key. Please check your key and try again.")
        elif response.status_code == 404:
            print(f"Error: City '{city}' not found.")
        return None
    except Exception as err:
        print(f"An other error occurred: {err}")
        return None

def create_visualization_dashboard(data):
    """Creates and saves a visualization dashboard from the weather data."""
    if not data:
        print("No data available to visualize.")
        return

    # Extracting the main data points
    main_weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    
    # Get current time for the title
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title = f"Weather Dashboard for {CITY_NAME.title()} at {timestamp}"

    # --- Create the Dashboard ---
    # Set the style
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6)) # 1 row, 2 columns of plots
    fig.suptitle(title, fontsize=16)

    # Plot 1: Temperature Bar Chart
    temp_data = {'Metric': ['Temperature (°C)', 'Feels Like (°C)'], 'Value': [temp, feels_like]}
    df_temp = pd.DataFrame(temp_data)
    sns.barplot(ax=axes[0], x='Metric', y='Value', data=df_temp, palette='coolwarm')
    axes[0].set_title('Temperature Information')
    axes[0].set_ylabel('Temperature (°C)')
    # Add value labels on top of bars
    for index, value in enumerate(df_temp['Value']):
        axes[0].text(index, value + 0.5, str(value), ha='center')

    # Plot 2: Humidity and Wind Speed
    other_data = {'Metric': ['Humidity (%)', 'Wind Speed (m/s)'], 'Value': [humidity, wind_speed]}
    df_other = pd.DataFrame(other_data)
    sns.barplot(ax=axes[1], x='Metric', y='Value', data=df_other, palette='viridis')
    axes[1].set_title('Humidity & Wind')
    axes[1].set_ylabel('Value')
    for index, value in enumerate(df_other['Value']):
        axes[1].text(index, value + 0.5, str(value), ha='center')
        
    # Add a text box with the general weather description
    fig.text(0.5, 0.02, f"Overall Weather: {main_weather} ({description})", ha='center', fontsize=12, style='italic')

    # Improve layout and save the figure
    plt.tight_layout(rect=[0, 0.05, 1, 0.95]) # Adjust layout to make space for suptitle and text
    plt.savefig('weather_dashboard.png')
    print("Dashboard saved as 'weather_dashboard.png'")
    
    # Show the plot
    plt.show()


# --- Main execution block ---
if __name__ == "__main__":
    weather_data = fetch_weather_data(API_KEY, CITY_NAME)
    
    # If we successfully got data, create the dashboard
    if weather_data:
        create_visualization_dashboard(weather_data)