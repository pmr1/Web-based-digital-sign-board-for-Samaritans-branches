This software extracts data from www.3r.org.uk to display the weekly rota and news items.
The rota table is displayed on a web page whose data is populated by a python programme running 
under flash ver 2.0.1. It runs on a raspberry pi4 running a linux distro ubuntu Mate 20.04.  It updates this page via a python script
every 2 hours through a crontab task.  In addition session times from the rota are used to control the central heating system via 
a wifi connected unit useing a esp8266 variant ( esp3).  Those dependents with suffix & are python modules in this version.

Note this should also run on a raspberry pi3 

The author suggests this is generic enough to extract any data from any web source to provide a local updated digital sign board


# Code files
local home directory (LHD) is /home/your local directory 
  
	scrape79.py  # resides in local home directory
	dependencies
   		json 
   		from datetime import *; from dateutil.relativedelta import *
   		config
   		calendar
   		dateutil.parser
   		from dateutil.parser import parse
   		requests
   writeCfg35M as WC
	 writeCfg35M.py # resides in LHD   &
	 no dependencies
	 
	 centralHeatControl31.py   # resides in local home directory
	 dependencies
	 	remoteControl46M as ChC # central heating control &
	 	encrypt7mod as E  # message encryption &
		dateutil.relativedelta import * 
		datetime import *
		ast import literal_eval
		time
		config
	remoteControl46M.py  # resides in local home directory
	#it assumes wifi linked central heat controller running in micropython on esp8266
	dependencies
		config
		socket
		datetime
		time
		re
		encrypt7mod as E &
		config
		writeCfgM35 as WC  &

# Timed File Sequence by crontab

	*/5 * * * * /usr/bin/python3 /home/LHD/python3/centralHeatControl31.py >> /home/LHD/indexPages/cronLog1.txt 2>&1
	3 * * * * /usr/bin/python3 /home/LHD/python3/scrape79.py >> /home/LHD/indexPages/cronLog1.txt 2>&1
	*/20 * * * * /home/lHD/measCoreTemp2.py >> /home/LHD/indexPages/cronLog1.txt 2>&1

data files generated by scrape79.py reside in /home/LHD/indexPages.
Log file from crontab is located /home/LHD/indexPages/cronLog1.txt

# Web apps
Samboard161.py via FlaskApp f
	assumes page <name>  (file /var/www/html/FlaskApps/templates/table31.html )
www/Samboar161.py  # resides in /var/www/html/FlaskApps directory

	The /var/www/html/indexPages are linked to a the local home directory
	/home/LHD/indexPages
	dependencies
		flask 
		Flask, 
		render_template, 
		jsonify, request
		ast import literal_eval
		time
		readChStateM16 as CHS &
		config
# Micropython
	The central heating controller running micropython, is built around esp03 ( esp8266 variant) and provides zero crossing switch 
	triac control of central heating system. See circuits. Cad files for the pcb are available in gerber format on request
	
	esp8266
		main280621.py
	dependences
		encrypt7Mod.py &
		
	
