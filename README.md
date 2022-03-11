This software extracts data from www.3r.org.uk to display the weekly rota and news items
The rota table is displayed on a web page whose date is populated by a python programme running 
under flash ver 2.0.1. It runs on a raspberry pi4 running a linux distro ubuntu Mate 20.04.  It updates this page via a python script
every 2 hours via a crontab task.  In addition session times from the rota are used to control the central heating system via 
a wifi connected unit useing a esp8266 variant ( esp3) 

Note this should also run on a raspberry pi3 

The author suggests this is generic enough to extract any data from any web source to provide a local updated digital sign board
