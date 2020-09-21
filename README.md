# E-paper Weather Display
Raspberry Pi weather display using Waveshare e-paper 7.5 inch display and Open Weather Map API and Python. 

# Setup
The first thing you need is a free API key from https://home.openweathermap.org/users/sign_up.
Open 'weather.py' and replace ******Key Here****** with your API key at line 52.
Location can be left as it is unless you want to add it to your display.
Get your longitude and lattitude using I used https://www.latlong.net and put that in as well. 

That's about it. Run the python file and you should see output on the display. 

# Note 
If you are not using a 7.5 inch Version 2 display, you will want to replace 'epd7in5_V2.py' in the 'lib' folder with whichever one you have from https://github.com/waveshare/e-Paper/tree/master/RaspberryPi%26JetsonNano/python/lib/waveshare_epd
