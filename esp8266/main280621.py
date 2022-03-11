'''
remote control unit
timer interrupts to blink led
encrypted version
feedback taps your feeback taps, start your start code, search chr
'''

import machine
from machine import Pin
import socket
import network
import time
from machine import ADC
cntrl1 = Pin (13,Pin.OUT)
# GPIO12 crashes esp03 because it doubles as MTDI, HSPI1_MISO
cntrl0 = Pin (14,Pin.OUT)  
ledRed = Pin(16,Pin.OUT)
ledGreen =Pin(2,Pin.OUT)
ledBlue = Pin(14,Pin.OUT)
pin2 =Pin(2,Pin.OUT)
pin14 =Pin(14,Pin.OUT)
import encrypt7Mod as E
ver = 'main280621.py'



	
def connectToWlan():
        lC1 = 'ZyXEL8D3D8C'
        pw1 = 'BDA6437712EB'
        lC2 = 'Gordon_F_Bennett'
        pw2 = 'Sherry_the_cat_1'
        global wlanAddr
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        # Scan for available access pointslocat
        # sta_if.scan()  
        # Connect to an AP
        sta_if.connect(lC2,pw2)
        time.sleep(7) # wait a while for connection
        # Check for successful connection
        C=sta_if.isconnected()  
        wlanAddr=sta_if.ifconfig()[0]
        return(C)

def readADC():
   adc = ADC(0)
   val = adc.read()
   return(val)
   
def tcb(timer):
        global tcounter,ledBlink
        # only counts when power is on.
        tcounter += 1
        ledBlink = ledBlink ^ True
        ledRed.value(ledBlink)
     
                
def setBlinky(To):
        global t1
        if To:		
                try:
                        # print(t1.isrunning()) this is no atribute of isrunning of timers contrary to documentation
                        t1.init(period =1000, mode=t1.PERIODIC, callback=tcb)
                        print(" timer started")

                except OSError:
                        t1.deinit()
                        print("timer failed hardware reset required")
        else:
                t1.deinit()
                print(" timer stopped")

def control0(state):
    if state:
        cntrl0.value(1)
    else:
        cntrl0.value(0)
        
def control1(state):
    if state:
        cntrl1.value(1)
    else:
        cntrl1.value(0)

def setServer(host,port):
        addr = socket.getaddrinfo(host, port)[0][-1]
        try:
            s = socket.socket()
        except OSError:
            s = None
            print ("1",exc.args[0])
        try:
            s.bind(addr)  # listens for ever
            s.listen(1)
        except OSError:
            #print ("2",exc.args[0])
            s.close()
            s = None
        
        if s is None:
            print ('could not open socket')
            # sys.exit(1)
            return(False)
        else:
            print("remote unit connected at ",addr )
            E.setFeedBack(0x96)
            E.check('*')
        while True:
                conn, addr = s.accept()
                # continues only when it receives a request
                print ('Connected by', addr)
                           #time.sleep(1)
                data = None
                while data == None:
                           data = conn.recv(1024)
                           #print (data)
                           # use  f = s.find(' ')
                           #  int(s[6:len(s)])  where s = filter 12
                           #dataStr = repr(data)  # converts the  non string data into a string
                           mesg = data.decode("utf-8")
                           #print (mesg)
                           dataStr = E.findMesg(mesg)
                           #print (dataStr)
                           if dataStr =="":
                              continue
                           else:
                                if dataStr == "*Heat on":
                                   rcvd = '*OK_ON'
                                   control0(True)
                                elif dataStr == "*Heat off":
                                   rcvd = '*OK_OFF'
                                   control0(False)
                                else :
                                    rcvd = "*Nok"
                           mesg = E.encryptMesg(rcvd,18)
                           conn.send(mesg)
                           conn.close()
        s.close()

#if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#   print('woke from a deep sleep')
t1 =machine.Timer(-1)
  # led indicating network connection ok
tcounter =0
ledBlink = False
ledBlink1 = 0
pin2.value(0)
pin14.value(0)
cntrl0.value(0)
cntrl1.value(0)
c= connectToWlan()
if c:
        setBlinky(True)
        setServer(wlanAddr,5000)
