'''
central heatning control

1. read times
2. if now
    send encrypted command to remote
    wait for acknowlegement
goto 1
dependencies remoteControl437M, encypt7mod , temperature2m

rolling code start
in reality it doen't matter what start number you provide providing the remote end
knows  .. could it do a code search to determine the start point
no code start
run locally in samvols
for use with crontab
added leading 0 in for hours < 10
coping with times in early hours next day
different reading style of for remoteControl433M
added temperature reading
control CH state by room temp
'''
ver = ' centralHeatControl31.py 050122 '
import remoteControl46M as ChC # central heating control
import encrypt7mod as E  # message encryption
import temperature2m as GT
import writeCfg35M as WC
import readChStateM16 as CHS
from dateutil.relativedelta import *
from datetime import *
from ast import literal_eval
import time
import config

rThres = 1.0  # threshold of to turn on heat
indexDir ='/home/user name/indexPages/'

chFile ='cHconfig.cfg'


def onOfftime(s):
    # string being split 7:45-11:0
    onTime = s.split("-")[0]
    onTi = int(onTime.split(':')[0])*60 + int(onTime.split(':')[1])
    offTime = s.split("-")[1]
    #print("on ",onTime,offTime)   
    offTi =int(offTime.split(':')[0])*60 + int(offTime.split(':')[1])
    #print("on off", onTi, offTi)
    return onTi, offTi

def determineCHstate(t):
    global wasdate
    NOW=datetime.now()
    sdate = NOW.strftime("%Y-%m-%d")
    stime = NOW.hour*60 + NOW.minute #strftime('%-H:%M')
    timdat = t.split(" ")
    #chState =None
    # determin time and date for early hours from day before
    on, off = onOfftime(timdat[1])
    #print(on,off)
    if off < on:    
         off = off+1440 
         WAS=NOW+relativedelta(days=-1)
         wasdate = WAS
         sdate = WAS.strftime("%Y-%m-%d")
         #print(on, off)
    # determine day and time
    if timdat[0] ==sdate:
        print(sdate, on,off, stime<= off)
        if CHS.getState(chFile,'temp') != 'no temp':
            print('cfg t ',CHS.getState(chFile,'temp'))
            roomTemp = float(CHS.getState(chFile,'temp'))
        else:
            roomTemp = 99
        setTemp  = float(CHS.getState(chFile,'setTemp'))
        #print('rt:', roomTemp, setTemp)
        if stime > on and stime <= off and (roomTemp < (setTemp + rThres)):
            chState = True
        else:
            chState = False
    else:
        chState = False
    return chState


global wasdate
wasdate ="no date"
#cht=open(indexDir+"centralHeat.txt","r")
cht=open(indexDir+"centralHeat1.txt","r")
datelist =[]
dataList = list(literal_eval(cht.readline()))
cht.close()
# prep encryption
E.check('*')
E.setFeedBack(0x96)
temp=GT.getTemp() 
WC.writeConfig(chFile,'temp:'+ "'"+temp+"'")
print('temp now',CHS.getState(chFile,'temp'))
for i in range(len(dataList)):
        state = determineCHstate(dataList[i])
        if state:
            res=ChC.heatCommand("on")
            break
        else:
            res=ChC.heatCommand("off")

#print(ChC.getChState())
NOW=datetime.now()
sdate = NOW.strftime("%Y-%m-%d")
stime = NOW.strftime('%H:%M')
print(sdate,stime,ChC.getChState(),'Room Temp :',temp)
#print(i,dataList[i])

    
