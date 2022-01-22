# This little program is for the Waveshare 7.5
# inch Version 2 black and white only epaper display
# It uses OpenWeatherMap API to display weather info
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
icondir = os.path.join(picdir, 'icon')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

# Search lib folder for display driver modules
sys.path.append('lib')
from waveshare_epd import epd7in5_V2
epd = epd7in5_V2.EPD()

from datetime import datetime
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import requests, json
from io import BytesIO
import csv

# define funciton for writing image and sleeping for 5 min.
def write_to_screen(image, sleep_seconds):
    print('Writing to screen.')
    # Write to screen
    h_image = Image.new('1', (epd.width, epd.height), 255)
    # Open the template
    screen_output_file = Image.open(os.path.join(picdir, image))
    # Initialize the drawing context with template as background
    h_image.paste(screen_output_file, (0, 0))
    epd.init()
    epd.display(epd.getbuffer(h_image))
    # Sleep
    time.sleep(2)
    epd.sleep()
    print('Sleeping for ' + str(sleep_seconds) +'.')
    time.sleep(sleep_seconds)

# define function for displaying error
def display_error(error_source):
    # Display an error
    print('Error in the', error_source, 'request.')
    # Initialize drawing
    error_image = Image.new('1', (epd.width, epd.height), 255)
    # Initialize the drawing
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source +' ERROR', font=font50, fill=black)
    draw.text((100, 300), 'Retrying in 30 seconds', font=font22, fill=black)
    current_time = datetime.now().strftime('%H:%M')
    draw.text((300, 365), 'Last Refresh: ' + str(current_time), font = font50, fill=black)
    # Save the error image
    error_image_file = 'error.png'
    error_image.save(os.path.join(picdir, error_image_file))
    # Close error image
    error_image.close()
    # Write error to screen
    write_to_screen(error_image_file, 30)

# Set the fonts
font22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
font35 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 35)
font50 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 50)
font60 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 60)
font100 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 100)
font160 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 160)

# Set the colors
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
grey = 'rgb(235,235,235)'

# Initialize and clear screen
print('Initializing and clearing screen.')
epd.init()
epd.Clear()

### Config ###
API_KEY = '******API KEY*******'
LOCATION = '*******'
LATITUDE = '*******'
LONGITUDE = '*******'
SCREEN_REFRESH = 600
CSV_OPTION = False
# set to 'metric','imperial', or 'standard' for kelvin 
UNITS = 'imperial'

BASE_URL = 'http://api.openweathermap.org/data/2.5/onecall?' 
URL = BASE_URL + 'lat=' + LATITUDE + '&lon=' + LONGITUDE + '&units=' + UNITS +'&appid=' + API_KEY

# dynamically set sign based on imperial or metric units
# - https://openweathermap.org/api/one-call-api#data
UNITS_SIGN = ''
UNITS_WINDSPEED = ''
if UNITS == 'imperial':
    UNITS_SIGN = 'F'
    UNITS_WINDSPEED = 'MPH'
elif UNITS == 'metric':
    UNITS_SIGN = 'C' 
    UNITS_WINDSPEED = 'M/sec'
else:
    UNITS_SIGN = 'K' 
    UNITS_WINDSPEED = 'M/sec'


while True:
    # Ensure there are no errors with connection
    error_connect = True
    while error_connect == True:
        try:
            # HTTP request
            print('Attempting to connect to OWM.')
            response = requests.get(URL)
            print('Connection to OWM successful.')
            error_connect = None
        except:
            # Call function to display connection error
            print('Connection error.')
            display_error('CONNECTION') 
    
    error = None
    while error == None:
        # Check status of code request
        if response.status_code == 200:
            print('Connection to Open Weather successful.')
            # get data in jason format
            data = response.json()
            
            # get current dict block
            current = data['current']
            # get current
            temp_current = current['temp']
            # get feels like
            feels_like = current['feels_like']
            # get humidity
            humidity = current['humidity']
            # get pressure
            wind = current['wind_speed']
            # get description
            weather = current['weather']
            report = weather[0]['description']
            # get icon url
            icon_code = weather[0]['icon']
            #icon_URL = 'http://openweathermap.org/img/wn/'+ icon_code +'@4x.png'
            
            # get daily dict block
            daily = data['daily']
            # get daily precip
            daily_precip_float = daily[0]['pop']
            #format daily precip
            daily_precip_percent = daily_precip_float * 100
            # get min and max temp
            daily_temp = daily[0]['temp']
            temp_max = daily_temp['max']
            temp_min = daily_temp['min']
            
            # Append weather data to CSV if csv_option == True
            if CSV_OPTION == True:
                # Get current year, month, date, and time
                current_year = datetime.now().strftime('%Y')
                current_month = datetime.now().strftime('%m')
                current_date = datetime.now().strftime('%d')
                current_time = datetime.now().strftime('%H:%M')
                #open the CSV and append weather data
                with open('records.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow([current_year, current_month, current_date, current_time,
                                     LOCATION,temp_current, feels_like, temp_max, temp_min,
                                     humidity, daily_precip_float, wind])
                print('Weather data appended to CSV.')
            
            # Set strings to be printed to screen
            string_location = LOCATION
            string_temp_current = format(temp_current, '.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN
            string_feels_like = 'Feels like: ' + format(feels_like, '.0f') +  u'\N{DEGREE SIGN}' + UNITS_SIGN
            string_humidity = 'Humidity: ' + str(humidity) + '%'
            string_wind = 'Wind: ' + format(wind, '.1f') + ' ' + UNITS_WINDSPEED
            string_report = 'Now: ' + report.title()
            string_temp_max = 'High: ' + format(temp_max, '>.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN
            string_temp_min = 'Low:  ' + format(temp_min, '>.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN
            string_precip_percent = 'Precip: ' + str(format(daily_precip_percent, '.0f'))  + '%'
            
            # Set error code to false
            error = False
            
        else:
            # Call function to display HTTP error
            display_error('HTTP')

    # Open template file
    template = Image.open(os.path.join(picdir, 'template.png'))
    # Initialize the drawing context with template as background
    draw = ImageDraw.Draw(template)
    
    # Draw top left box
    ## Open icon file
    icon_file = icon_code + '.png' 
    icon_image = Image.open(os.path.join(icondir, icon_file))
    ### Paste the image
    template.paste(icon_image, (40, 15))
    ## Place a black rectangle outline
    draw.rectangle((25, 20, 225, 180), outline=black)
    ## Draw text
    draw.text((30, 200), string_report, font=font22, fill=black)
    draw.text((30, 240), string_precip_percent, font=font30, fill=black)
    # Draw top right box
    draw.text((350, 210), string_feels_like, font=font50, fill=black)
    
    # detect minus in metric and adjust screen
    if (UNITS == 'metric') and ( int(temp_current) < 0):
        draw.text((340, 35), string_temp_current, font=font160, fill=black)
    elif (UNITS == 'imperial') or (UNITS == 'metric'):
        draw.text((375, 35), string_temp_current, font=font160, fill=black)
    else:
        #need more space for kelvin
        draw.text((310, 35), string_temp_current, font=font160, fill=black)

    # Draw bottom left box
    draw.text((35, 325), string_temp_max, font=font50, fill=black)
    draw.rectangle((170, 385, 265, 387), fill=black)
    draw.text((35, 390), string_temp_min, font=font50, fill=black)
    # Draw bottom middle box
    draw.text((345, 340), string_humidity, font=font30, fill=black)
    draw.text((345, 400), string_wind, font=font30, fill=black)
    # Draw bottom right box
    draw.text((627, 330), 'UPDATED', font=font35, fill=white)
    current_time = datetime.now().strftime('%H:%M')
    draw.text((627, 375), current_time, font = font60, fill=white)

    ## Add a reminder to take out trash on Mon and Thurs
    weekday = datetime.today().weekday()
    if weekday == 0 or weekday == 3:
        draw.rectangle((345, 13, 705, 55), fill =black)
        draw.text((355, 15), 'TAKE OUT TRASH TODAY!', font=font30, fill=white)
        
    # Save the image for display as PNG
    screen_output_file = os.path.join(picdir, 'screen_output.png')
    template.save(screen_output_file)
    # Close the template file
    template.close()
    
    # Refresh clear screen to avoid burn-in at 3:00 AM
    if datetime.now().strftime('%H') == '03':
        print('Clearning screen to avoid burn-in.')
        epd.Clear()
    
    # Write to screen
    write_to_screen(screen_output_file, SCREEN_REFRESH)
