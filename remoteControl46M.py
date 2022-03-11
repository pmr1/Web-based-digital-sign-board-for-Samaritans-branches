'''
remote control via wifi
remote unit example esp03
with encryption
input command output received state
for use as a module
'''
import config
import socket
import datetime
import time
import re # regular expression
import encrypt7mod as E
import config
import writeCfg35M as WC

chFile ='cHconfig.cfg'
#lockFile ='lockState.cfg'

ver ='remoteControl46M.py 060122'

remote_address='your lan address', 5000
#indexDir ='/home/samsrpi/indexPages/'
indexDir ='/home/your user name/indexPages/'  # normal linux user

def remoteHost(mesg,serverAddress):
    indexDir ='/home/your user name/indexPages/'  # normal linux user
    # assuming wired connection
    # mesg as ascii text
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(1)
    state = False
    try:
        s.connect(serverAddress)
        state = True
    except OSError as e:
        s = None
        state = False
        #print ("no connection from "+str(serverAddress))
        Returned=E.encryptMesg("*off line",18)

    if state:  # socket open
        c = 1
        while c < 2:
            c = c + 1
            sData = mesg
            s.send(sData.encode())
            time.sleep(0.5)
            try:
                data = s.recv(1024)
                state = True
            except OSError:
                s = None
                state = False
            if state:
                dataStr = data.decode("utf-8")
                Returned = dataStr
            #print('Received ',dataStr )
                return Returned
            else:
                Returned = E.encryptMesg('*off line',18)
                c = 2
        #s.close()
    else:  
        return Returned


def heatCommand(cmd):
    global chS
    if cmd=="on":
        cypherMessage=E.encryptMesg("*Heat on",18)
        m = remoteHost(cypherMessage,remote_address)
        plainText = E.findMesg(m)
        #print(plainText)
        if plainText != 'off line':
        # update external ch state
            cdata = plainText[1:len(plainText)]
            cfgData ='chState:'+"'"+cdata+"'"     
            res = WC.writeConfig(chFile,cfgData)
            #print('h0',cfgData,res)
        else:
            res = WC.writeConfig(chFile,plainText)
    elif cmd=="off":
        cypherMessage=E.encryptMesg("*Heat off",XX) # XX is start code fore encryption and decryption
        m = remoteHost(cypherMessage,remote_address)
        plainText = E.findMesg(m)
        #print(plainText)
        if plainText != '*off line':
        # update external ch state
            cdata = plainText[1:len(plainText)]
            cfgData ='chState:'+"'"+cdata+"'"
            res = WC.writeConfig(chFile,cfgData)
            #print('h1',cfgData,res)
        else:
            cfgData ='chState:'+ plainText
            cdata = plainText
            cfgData ='chState:'+"'"+cdata+"'"
            res = WC.writeConfig(chFile,cfgData)
            
    else:
        plainText = "*no change"
    if res == plainText:  # if rex != plainText then external ch state is missing
       chS = plainText 
       return plainText         
    else:
        chS = plainText 
        return res
   
def getChState():
    global chS
    import config
    chS = "no change"
    indexDir ='/home/your user name/indexPages/'  # normal linux user
    cfg = config.Config(indexDir+chFile)
    return cfg['chState']
    


