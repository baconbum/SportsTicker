#!/bin/bash
# Install prerequisites for SportsTicker

echo "Installing apt-get packages: python3, python3-pip, sqlite3"
echo
apt-get install python3 python3-pip sqlite3
echo

echo "Installing pip3 packages: RPLCD RPi.GPIO pytz requests"
echo
pip3 install RPLCD RPi.GPIO pytz requests
