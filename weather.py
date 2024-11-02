import os
import sys
import csv
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests

# Automatically add the 'lib' directory relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, 'lib')
sys.path.append(lib_path)
from waveshare_epd import epd7in5_V2
epd = epd7in5_V2.EPD()

# User defined configuration
API_KEY = 'XXXXXXXX'  # Your API key for openweathermap.com
LOCATION = 'XXXXXXXX'  # Name of location
LATITUDE = 'XXXXXXXX'  # Latitude
LONGITUDE = 'XXXXXXXX'  # Longitude
UNITS = 'imperial' # imperial or metric
CSV_OPTION = True # if csv_option == True, a weather data will be appended to 'record.csv'
TRASH_DAYS = [2]  # 0 = Monday, 6 = Sunday; Multiple days can be passed as a list

BASE_URL = f'https://api.openweathermap.org/data/3.0/onecall'
FONT_DIR = os.path.join(os.path.dirname(__file__), 'font')
PIC_DIR = os.path.join(os.path.dirname(__file__), 'pic')
ICON_DIR = os.path.join(PIC_DIR, 'icon')

# Initialize display
epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()

# Logging configuration for both file and console
LOG_FILE = 'weather_display.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use RotatingFileHandler for log rotation
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)  # 1MB file size, 3 backups
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(file_handler)

# Stream handler for logging to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(console_handler)

logger.info("Weather display script started.")

# Set fonts with specific sizes to match the old behavior
font22 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 22)
font30 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 30)
font35 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 35)
font50 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 50)
font60 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 60)
font100 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 100)
font160 = ImageFont.truetype(os.path.join(FONT_DIR, 'Font.ttc'), 160)
COLORS = {'black': 'rgb(0,0,0)', 'white': 'rgb(255,255,255)', 'grey': 'rgb(235,235,235)'}

# Fetch weather data
def fetch_weather_data():
    url = f"{BASE_URL}?lat={LATITUDE}&lon={LONGITUDE}&units={UNITS}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Weather data fetched successfully.")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
        raise

# Process weather data
def process_weather_data(data):
    try:
        current = data['current']
        daily = data['daily'][0]
        weather_data = {
            "temp_current": current['temp'],
            "feels_like": current['feels_like'],
            "humidity": current['humidity'],
            "wind": current['wind_speed'],
            "report": current['weather'][0]['description'].title(),
            "icon_code": current['weather'][0]['icon'],
            "temp_max": daily['temp']['max'],
            "temp_min": daily['temp']['min'],
            "precip_percent": daily['pop'] * 100,
        }
        logging.info("Weather data processed successfully.")
        return weather_data
    except KeyError as e:
        logging.error(f"Error processing weather data: {e}")
        raise

# Save weather data to CSV
def save_to_csv(weather_data):
    if not CSV_OPTION:
        return
    try:
        with open('records.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                LOCATION,
                weather_data["temp_current"],
                weather_data["feels_like"],
                weather_data["temp_max"],
                weather_data["temp_min"],
                weather_data["humidity"],
                weather_data["precip_percent"],
                weather_data["wind"]
            ])
        logging.info("Weather data appended to CSV.")
    except IOError as e:
        logging.error(f"Failed to save data to CSV: {e}")

# Generate display image
def generate_display_image(weather_data):
    try:
        template = Image.open(os.path.join(PIC_DIR, 'template.png'))
        draw = ImageDraw.Draw(template)
        icon_path = os.path.join(ICON_DIR, f"{weather_data['icon_code']}.png")
        icon_image = Image.open(icon_path) if os.path.exists(icon_path) else None

        if icon_image:
            template.paste(icon_image, (40, 15))

        draw.text((30, 200), f"Now: {weather_data['report']}", font=font22, fill=COLORS['black'])
        draw.text((30, 240), f"Precip: {weather_data['precip_percent']:.0f}%", font=font30, fill=COLORS['black'])
        draw.text((375, 35), f"{weather_data['temp_current']:.0f}°F", font=font160, fill=COLORS['black'])
        draw.text((350, 210), f"Feels like: {weather_data['feels_like']:.0f}°F", font=font50, fill=COLORS['black'])
        draw.text((35, 325), f"High: {weather_data['temp_max']:.0f}°F", font=font50, fill=COLORS['black'])
        draw.text((35, 390), f"Low: {weather_data['temp_min']:.0f}°F", font=font50, fill=COLORS['black'])
        draw.text((345, 340), f"Humidity: {weather_data['humidity']}%", font=font30, fill=COLORS['black'])
        draw.text((345, 400), f"Wind: {weather_data['wind']:.1f} MPH", font=font30, fill=COLORS['black'])
        draw.text((627, 330), "UPDATED", font=font35, fill=COLORS['white'])
        current_time = datetime.now().strftime('%H:%M')
        draw.text((627, 375), current_time, font=font60, fill=COLORS['white'])

        # Trash reminder based on TRASH_DAYS config
        weekday = datetime.today().weekday()
        if weekday in TRASH_DAYS:
            draw.rectangle((345, 13, 705, 55), fill=COLORS['black'])
            draw.text((355, 15), 'TAKE OUT TRASH TODAY!', font=font30, fill=COLORS['white'])
        
        logging.info("Display image generated successfully.")
        return template
    except Exception as e:
        logging.error(f"Error generating display image: {e}")
        raise

# Display image on screen
def display_image(image):
    try:
        h_image = Image.new('1', (epd.width, epd.height), 255)
        h_image.paste(image, (0, 0))
        epd.display(epd.getbuffer(h_image))
        logging.info("Image displayed on e-paper successfully.")
    except Exception as e:
        logging.error(f"Failed to display image: {e}")
        raise

# Main function
def main():
    try:
        data = fetch_weather_data()
        weather_data = process_weather_data(data)
        save_to_csv(weather_data)
        image = generate_display_image(weather_data)
        display_image(image)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()