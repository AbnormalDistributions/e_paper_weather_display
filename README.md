<h1>E-paper Weather Display</h1>
<br>
  Raspberry Pi weather display using Waveshare e-paper 7.5 inch display, Open Weather Map API, and Python.
<img src="https://github.com/AbnormalDistributions/e_paper_weather_display/blob/master/photo.jpg" width=75% height=75%> <br>

<h1>Versions</h1>
  <h2>Version 1.0</h1>
    <ul>
	  <li>Initial Commit</li>
	</ul>
  <h2>Version 1.1</h1>
    <ul>
      <li>Added more legible icons</li>
    </ul>


<h1>Setup</h1>
<ol>
  <li>The first thing you need is a free API key from https://home.openweathermap.org/users/sign_up.</li>
  <li>Open 'weather.py' and replace **Key Here** with your API key at line 52.</li>
  <li>**Location** can be left as it is unless you want to add it to your display.</li>
  <li>Get your **longitude** and **lattitude** using I used https://www.latlong.net and put that in as well.</li>
  <li>Line 176 has a reminder for taking out the trash as well that you will want to change if your trash pickup doesn't come on Monday and Thursday like mine. :)</li>
</ol>
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

<h1>Credit</h1>
  Icon designs are originally by [Erik Flowers] (https://erikflowers.github.io/weather-icons/). Some icons have been modified. 

<h1>Licensing</h1>
  <ul>
    <li>Weather Icons licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL)</li>
    <li>Code licensed under [MIT License](http://opensource.org/licenses/mit-license.html)</li>
    <li>Documentation licensed under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0)</li>
  <ul>