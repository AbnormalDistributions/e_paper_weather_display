<h1>E-paper Weather Display</h1>
<br>
  Raspberry Pi weather display using Waveshare e-paper 7.5 inch display, Open Weather Map API, and Python.
<img src="https://github.com/AbnormalDistributions/e_paper_weather_display/blob/master/photo.jpg" width=75% height=75%> <br>

<h1>Setup</h1>
The first thing you need is a free API key from https://home.openweathermap.org/users/sign_up.<br>
Open 'weather.py' and replace **Key Here** with your API key at line 52.<br>
**Location** can be left as it is unless you want to add it to your display.<br>
Get your **longitude** and **lattitude** using I used https://www.latlong.net and put that in as well.<br>
Line 176 has a reminder for taking out the trash as well that you will want to change if your trash pickup doesn't come on Monday and Thursday like mine. :)<br>
<br>
That's about it. Run the python file and you should see output on the display. 

# Note 
If you are not using a 7.5 inch Version 2 display, you will want to replace 'epd7in5_V2.py' in the 'lib' folder with whichever one you have from https://github.com/waveshare/e-Paper/tree/master/RaspberryPi%26JetsonNano/python/lib/waveshare_epd<br>
Fairly extensive adjustments will have to be made for other sized screens.

# Parts
<ol>
  <li>https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT</li>
  <li>Raspberry Pi 3, but this will run on any of them except the Pi Zero that doesn't have soldered headers.</li>
  <li>SD card for the Pi at least 8 GB.</li>
  <li>Power supply for the Pi.</li>
</ol>
