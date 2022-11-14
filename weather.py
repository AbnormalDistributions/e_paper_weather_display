#!/usr/bin/python

# This little program is for the Waveshare 7.5
# inch Version 2 black and white only epaper display
# It uses OpenWeatherMap API to display weather info
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO

import traceback
import requests, json
import time
import sys
import os

sys.path.append('lib')
from waveshare_epd import epd7in5_V2
epd = epd7in5_V2.EPD()

# Variables
BASE_URL = 'http://api.openweathermap.org/data/2.5/onecall?' 
#Free API only updates 1 per 2 hours - https://openweathermap.org/full-price#current

#Set screen refresh freuqncy 
screen_refresh_min = 5

#API key for http://api.openweathermap.org/data/2.5/onecall?' 
API_KEY = 'XXXX'

#screen stuff 
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

# Screen colors
black = 'rgb(0,0,0)'
white = 'rgb(255,255,255)'
grey = 'rgb(235,235,235)'

#Choose 'metric','imperial', or 'standard' for kelvin 
UNITS = 'metric'
if UNITS == 'imperial':
    UNITS_SIGN = 'F'
    UNITS_WINDSPEED = 'MPH'
elif UNITS == 'metric':
    UNITS_SIGN = 'C' 
    UNITS_WINDSPEED = 'M/sec'
else:
    UNITS_SIGN = 'K' 
    UNITS_WINDSPEED = 'M/sec'

#generate URL
#URL = BASE_URL + 'lat=' + LATITUDE + '&lon=' + LONGITUDE + '&units=' + UNITS +'&appid=' + API_KEY
URL = BASE_URL + 'lat=' + '44.977753' + '&lon=' + '-93.265015' + '&units=' + UNITS +'&appid=' + API_KEY


# define function for displaying error
def display_error(error_source):
    print('[ ERROR ] : request ', error_source)
    error_image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(error_image)
    draw.text((100, 150), error_source +' ERROR', font=font50, fill='rgb(0,0,0)')
    draw.text((100, 300), 'Retrying in 30 seconds', font=font22, fill=black)
    current_time = datetime.now().strftime('%H:%M')
    draw.text((300, 365), 'Last Refresh: ' + str(current_time), font = font50, fill=black)
    error_image_file = 'error.png'
    error_image.save(os.path.join(picdir, error_image_file))
    error_image.close()
    write_to_screen(error_image_file, 30)


def api_connect():
    try:
        response=requests.get(URL)
        print('[ SUCCESS  ] Connected to OWM')
        if response.status_code != 200:
            display_error('HTTP')
        print('[ SUCCESS  ] Refreshed API at : ' + str(datetime.now()))
        return response
    except:
        display_error('CONNECTION') 


# write image and sleep
def write_to_screen(image):
    screen_output_file = Image.open(os.path.join(picdir, image))
    print('[ REFRESH  ] Screen ' + str(datetime.now()))
    epd.init()
    h_image = Image.new('1', (epd.width, epd.height), 255)
    h_image.paste(screen_output_file, (0, 0))
    epd.display(epd.getbuffer(h_image))
    time.sleep(2)
    epd.sleep()


def debug_data(data):
    print('[ DEBUG    ] ' + str(datetime.now()))
    print "temp       : " + str(data['current']['temp'])
    print "temp_min   : " + str(data['daily'][0]['temp']['min'])
    print "temp_max   : " + str(data['daily'][0]['temp']['max'])
    print "feels_like : " + str(data['current']['feels_like'])
    print "precip     : " + str(data['daily'][0]['pop'] * 100)
    print "desc       : " + str(data['current']['weather'][0]['description'].title())
    print "dewpoint   : " + str(data['current']['dew_point'])
    print "sunrise    : " + datetime.fromtimestamp(data['current']['sunrise']).strftime('%I:%M %p')
    print "sunset     : " + datetime.fromtimestamp(data['current']['sunset']).strftime('%I:%M %p')


### screen stuff here ###
def prepare_screen(data):
    template = Image.open(os.path.join(picdir, 'template.png'))

    #font variables
    font22 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 22)
    font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
    font50 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 50)
    font60 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 60)
    font160 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 160)
    
    #Border
    ImageDraw.Draw(template).rectangle((25, 20, 225, 180), outline=black)

    #Left box
    ImageDraw.Draw(template).rectangle((170, 385, 265, 387), fill=black)

    #Icon in top left
    template.paste(Image.open(os.path.join(os.path.join(picdir, 'icon'), data['current']['weather'][0]['icon'] + '.png')), (40, 15))

    #detect minus in metric and adjust screen
    if (UNITS == 'metric') and ( data['current']['temp'], '.0f' < 0):
        ImageDraw.Draw(template).text((340, 35), format(data['current']['temp'], '.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN, font=font160, fill=black)
    elif (UNITS == 'imperial') or (UNITS == 'metric'):
        ImageDraw.Draw(template).text((375, 35), format(data['current']['temp'], '.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN, font=font160, fill=black)
    else:
        ImageDraw.Draw(template).text((310, 35), format(data['current']['temp'], '.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN, font=font160, fill=black)

    #draw text
    ImageDraw.Draw(template).text((30, 190), data['current']['weather'][0]['description'].title(), font=font22, fill=black)
    ImageDraw.Draw(template).text((30, 220), 'Rain : ' + str(format(data['daily'][0]['pop'] * 100, '.0f'))  + '%', font=font22, fill=black)
    ImageDraw.Draw(template).text((30, 250), 'Dew  : ' + str(data['current']['dew_point']) + u'\N{DEGREE SIGN}' + UNITS_SIGN, font=font22, fill=black)

    
    #top right
    ImageDraw.Draw(template).text((350, 210), 'Feels like: ' + format(data['current']['feels_like'], '.0f') +  u'\N{DEGREE SIGN}'  + UNITS_SIGN, font=font50, fill=black)
    
    #high
    ImageDraw.Draw(template).text((35, 325), 'High: ' + format(data['daily'][0]['temp']['max'], '>.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN, font=font50, fill=black)
    
    #low
    ImageDraw.Draw(template).text((35, 390), "Low : " + format(data['daily'][0]['temp']['min'], '>.0f') + u'\N{DEGREE SIGN}' + UNITS_SIGN, font=font50, fill=black)
    
    #bottom middle box
    ImageDraw.Draw(template).text((345, 340), 'Humidity: ' + str(data['current']['humidity']) + '%', font=font30, fill=black)
    ImageDraw.Draw(template).text((345, 400), 'Wind: ' + format(data['current']['wind_speed'], '.1f') + ' ' + UNITS_WINDSPEED, font=font30, fill=black)
    
    #bottom right
    ImageDraw.Draw(template).text((610, 305), 'sunset  ' + datetime.fromtimestamp(data['current']['sunset']).strftime('%I:%M %p') , font=font22, fill=white)
    ImageDraw.Draw(template).text((610, 327), 'sunrise ' + datetime.fromtimestamp(data['current']['sunrise']).strftime('%I:%M %p') , font=font22, fill=white)

    ##issue
    ImageDraw.Draw(template).text((620, 375), datetime.now().strftime('%H:%M'), font = font60, fill=white)

    #Send things to the screen
    screen_output = os.path.join(picdir, 'screen_output.png')
    template.save(screen_output)
    template.close()
    return screen_output


#Clear screen
def init_screen():
    print('[ INIT     ] Screen')
    epd.init()
    epd.Clear()


# refresh clock on the 5 mins
def sleep():
    current_time = datetime.now()
    #print 'time                : ' + str(current_time)
    #print 'current_time.minute : ' + str(current_time.minute)
    #print 'time % refresh      : ' + str(current_time.minute % screen_refresh_min)
    if ((current_time.minute % screen_refresh_min) == 0):
        print("[ SLEEPING ] " + str(screen_refresh_min - 1) + ' mins ' + str(60 - current_time.second) + ' sec')
        time.sleep(((screen_refresh_min - 1) * 60 ) + (60 - current_time.second))
    else: 
        print("[ SLEEPING ] " + str(screen_refresh_min - (current_time.minute % screen_refresh_min) - 1) + ' mins ' + str(60 - current_time.second) + ' sec')
        time.sleep(((screen_refresh_min - (current_time.minute % screen_refresh_min) - 1) * 60) + (60 - current_time.second))


def main():
    while True:
        print '[ TIME     ] ' + str(datetime.now())
        data = api_connect().json()
        debug_data(data)
        screen_output = prepare_screen(data)
        write_to_screen(screen_output)
        sleep()


### main ###
main()
