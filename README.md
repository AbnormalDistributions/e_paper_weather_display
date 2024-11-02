

# E-paper Weather Display

This project uses a Raspberry Pi to show weather updates and trash reminders on a Waveshare 7.5-inch e-paper display. It fetches weather data from OpenWeatherMap and refreshes the display at set intervals. Minimal energy consumption makes this setup ideal for continuous display without frequent updates.

![Display Photo 1](https://github.com/AbnormalDistributions/e_paper_weather_display/blob/master/photos/photo1.jpg?raw=true)
![Display Photo 2](https://raw.githubusercontent.com/AbnormalDistributions/e_paper_weather_display/refs/heads/master/photos/photo2.jpg)

If you find this project useful, consider [buying me a coffee ☕️](https://ko-fi.com/abnormaldistributions).

---

## Table of Contents
- [What’s New](#whats-new-version-20)
- [Parts List](#parts-list)
- [Setup Instructions](#setup-instructions)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Script](#running-the-script)
- [Setting up Automatic Updates (Cron)](#setting-up-automatic-updates-optional)
- [Repository Structure](#files-in-this-repository)
- [Troubleshooting](#troubleshooting)
- [Credit and License](#credit-and-license)

## What’s New (Version 2.0)
- **Upgraded to OpenWeatherMap One Call API 3.0**: This update now uses the latest version of the OpenWeatherMap API (3.0), which may require users to update their subscriptions if they were previously using version 2.5. See the [OpenWeatherMap One Call Migration Guide](https://openweathermap.org/one-call-transfer) for details on the API changes and subscription requirements.
- **Automatic Log Management**: Logs now rotate when they get too large, making maintenance easier.
- **User-Friendly Settings**: All essential settings are grouped together for quick customization.
- **More Reliable Error Handling**: Logs network and API errors for easier troubleshooting.
- **Improved Directory Handling**: The script finds the right directories automatically, without manual path adjustments.
- **Trash Day Reminders**: Customize specific days to get reminders on the display.

### Parts List
- **Waveshare 7.5-inch e-Paper HAT**: [Available on Amazon](https://amzn.to/3YuH1kA) (affiliate link).  
- **Raspberry Pi** (tested on a Pi 3; any model should work except the Pi Zero without soldered headers).
- **SD card** (at least 8 GB).
- **Power supply** for the Raspberry Pi.
- **5 x 7 inch photo frame** (thrift store find recommended).

> **Note**: If you use this affiliate link, it helps support this project at no additional cost to you. Thank you!


## Setup Instructions

### Installation
1. **Clone the Project**:
   Open a terminal and run:
   ```bash
   git clone https://github.com/AbnormalDistributions/e_paper_weather_display.git
   cd e_paper_weather_display
   ```

2. **Install Python Libraries**:
   ```bash
   pip install pillow requests
   ```

### Configuration
1. **Add Your OpenWeatherMap API Key**:
   Sign up on [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) for an API key, then open `weather.py` and add your API key where it says `API_KEY = 'XXXXXXXX'`.

2. **Customize Your Settings**:
   Edit the following user-defined settings at the top of `weather.py`:
   - `API_KEY`: Your OpenWeatherMap API key.
   - `LOCATION`: Name of the location to display (e.g., `New Orleans`).
   - `LATITUDE` and `LONGITUDE`: Coordinates for weather updates (use [Google Maps](https://maps.google.com) to find these).
   - `UNITS`: Choose `'imperial'` (Fahrenheit) or `'metric'` (Celsius).
   - `CSV_OPTION`: Set this to `True` if you’d like to save a daily log of weather data in `records.csv`.
   - `TRASH_DAYS`: Add the days for trash reminders as numbers (0=Monday, 6=Sunday).

> **Note**: If you are not using a 7.5 inch Version 2 display, you will want to replace 'epd7in5_V2.py' in the 'lib' folder with the appropriate version from [Waveshare's e-Paper library](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd). Adjustments will be required for other screen sizes.

## Running the Script
1. **To Run Manually**:
   From the `e_paper_weather_display` directory, run:
   ```bash
   python weather.py
   ```
   This will fetch the weather data and update the display immediately.

## Setting up Automatic Updates (Optional)
You can set up a scheduled update every 15 minutes using `crontab`. This will make sure your display updates automatically.

In the terminal, type:
```bash
crontab -e
```
Then, add the following line at the end of the file:
```bash
*/15 * * * * /usr/bin/python /home/pi/e_paper_weather_display/weather.py >> /home/pi/e_paper_weather_display/weather_display.log 2>&1
```
- This command updates the display every 15 minutes.
- Be sure to replace `/home/pi/e_paper_weather_display/` with the path where the project is stored, if different.

## Files in This Repository
- **weather.py**: Main script file that fetches weather data and updates the display.
- **lib/**: Contains display drivers for the Waveshare e-paper display.
- **font/** and **pic/**: Folders with fonts and images used by the display.
- **photos/**: Sample images of the display in action.
- **records.csv**: Optional log file for weather data if `CSV_OPTION` is enabled.

## Troubleshooting
- Make sure the **API_KEY** is correct and has permissions for OpenWeatherMap’s One Call API.
- Confirm that required Python libraries (`pillow` and `requests`) are installed.
- Double-check any custom paths used in `crontab` if the automatic updates aren’t working as expected.

## Credit and License
- Icon designs by [Erik Flowers](https://erikflowers.github.io/weather-icons/), with some modifications.
- **Weather Icons**: Licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL).
- **Code**: Licensed under [MIT License](http://opensource.org/licenses/mit-license.html).
- **Documentation**: Licensed under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0).
