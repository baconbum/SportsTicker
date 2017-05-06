# SportsTicker

## About
This project alerts users to live scoring play updates, as well as allow users to see the full daily schedule of the supported leagues. Full daily schedule includes current scores, time remaining in game, and (if the game is not yet started) start time. It uses several LEDs, an LCD, and a button connected to a Raspberry Pi running a Python 3 script to display relevant information.

Currently supports NHL score updates using the nhl.com REST API.

## Setup
1. Install Raspbian Jessie Lite on Raspberry Pi.
    * I tested using the April 2017 version of Raspbian Jessie Lite on a Raspberry Pi 2.
2. [Configure Wifi](https://thepihut.com/blogs/raspberry-pi-tutorials/83502916-how-to-setup-wifi-on-raspbian-jessie-lite) and [enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/).
3. Update OS: `sudo apt-get update && sudo apt-get upgrade && sudo apt-get autoremove`.
    * This step is optional, but recommended.
4. Download SportsTicker package from GitHub onto your Pi.
5. Run prerequisites script: `sudo bash installPrerequisites.sh`
6. Initialize database: `python3 initializeDatabase.py`
7. Connect 4 LEDs, 1 LCD and 1 button to your Pi.
    * Coming later: Picture tutorial of connecting hardware to Pi.
8. Customize config.ini to fit your setup.
9. Run main script to constantly check scores: `python3 main.py`
