'''
  from https://github.com/danjperron/BitBangingDS18B20
  with the modification of adding
#define PY_SSIZE_T_CLEAN  int
#include <Python.h>

to the DS18B20.c file in the python directory
  
'''

import time
import DS18B20 as DS
GPIO_PIN=4   # Raspberry pin GPIO

#sensors = DS.scan(4)
def findSensors():
    sensors=DS.scan(GPIO_PIN)
    return sensors

#print(findSensors())
def getTemp():
    try:
        sensors = findSensors()
        DS.pinsStartConversion([GPIO_PIN])
        time.sleep(0.25)
        for i in sensors:
          t= DS.read(False,GPIO_PIN,i)
          rt = round(t,3)
        return str(rt)
    except :
       return "no temp"

