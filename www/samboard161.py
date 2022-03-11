'''

Files as of the name but either prefixed with A or B
corrected call to get_rotasec missing buffer prefix
assumes flask ver 2.0.1 or later
'''
from flask import Flask, render_template, jsonify, request
from ast import literal_eval
#import datetime
import logging
import time
import readChStateM16 as CHS
import config

app = Flask(__name__)
#app.static_folder='/static/'
ver = 'samboard161.py 301221'
noEvents = '("no events found", '', '', '', '', '', '', '')'
nullTable = '("no data", '', '', '', '', '', '', '')'
dataDir ='/var/www/html/indexPages/'
#dataDir =''
newsCounter = 0
chFile ='cHconfig.cfg'


def get_week_dates(b):
# combines headFirst 'Monday ... with actual week dates
    global weekStart, weekEnd
    list2=[]
    fn = open(dataDir+b+"weekDates.txt", "r")
    #print(dataDir+b+"weekDates.txt")
    list = fn.readlines()
    fn.close()
    for line in list:
        list2.append(literal_eval(line))
    # list3 = list2[0]
    head = ['TIME  ','Monday       ','Tuesday       ','Wednesday     ', 'Thursday      ', 'Friday      ', 'Saturday       ', 'Sunday      ']
    #print(headFirst)
    j = 1;
    while j < 8:
        head[j] = head[j] + '|' + str(list2[0][j - 1])
        j = j + 1
    weekStart = str(list2[0][0])  ; weekEnd = str(list2[0][6])
    return tuple(head)

def get_leader_rota(b):
    fn = open(dataDir+b+"leadersRota.txt", "r")
    T1 = fn.readlines()   # only the first line but there could be 2 or more
    fn.close()
    list2=[]
    c=0
    for line in T1:
        list2.append(literal_eval(line))
    return tuple(list2)


def get_leader_support(b):
    # leader support combined with rota sec
    fn = open(dataDir+b+"leadersSupport.txt", "r")
    T1 = fn.readline()   # first line only read
    T2 = get_rotaSec(b)
    fn.close()
    ListT1 = list(literal_eval(T1))
    ListT2 = list(literal_eval(T2))
    ListT1[2] = ListT2[1]
    return tuple(ListT1)


def get_top_head():
    return tuple(headFirst)



def get_events(b):
    global getCount
    fn = open(dataDir+b+"events.txt", "r")
    lineList =[]
    lineList = fn.readlines()
    ln = noEvents
    try:
        for line in lineList:
            ln= literal_eval(line)
    except OSError:
        return noEvents
    return tuple(ln)

def get_rotaSec(b):
    fn=open(dataDir+b+"rotaSec.txt","r")
    l = fn.readline()
    fn.close()
    return l


def get_rota_data(b):
    # this should include headers
    fn = open(dataDir+b+"tableData.txt", "r")
    T1 = fn.readlines()
    # print(list)
    T2 = []

    for line in T1:
        # print (item)  # item and line are determine by \n in readline() and readlines()
        T2.append(tuple(literal_eval(line)))
    # print (da)
  
    return tuple(T2)
    
def get_news(b):
    global newsCounter
    # nc is a newsitem  counter the increments on each get cycle
    fn = open(dataDir+b+"newsData.txt", "r")
    T1 = fn.readlines()
    sizeofNews = len(T1)
    nc = newsCounter % sizeofNews
    newsCounter += 1
    ni = T1[nc].replace("[","")
    ni = T1[nc].replace("']","")
    ni = T1[nc].replace(',','')
    T2= ni.split('$$')
    return T2

    
    

def FileOk():
    # ok to read?
    lf = dataDir+chFile
    cfg = config.Config(lf)
    count = 0
    nok = True
    while nok and count < 10:
        cfg = config.Config(lf)
        nok = (cfg['fileState'] == 'unlocked')
        count +=1
        time.sleep(1)
    if not nok:
        return True
    else:
        return True
def getbuf():
     # read cfg file and determine which buffer prefix to use
     b= CHS.getState(chFile,'buffer')
     return b 

# but you can't have comments in the html file
# I can't use a while statement to check file ok it always hangs
# so I to use an single check and if statement  
@app.route('/index', methods=["GET"])
def table():
    global weekStart, weekEnd, lastevnt,lastrsd,lastlrd,lastlsr, newsCounter
    if request.method == "GET":
        print(newsCounter)
        b=getbuf()   # now working
        #b = 'A'
        head = get_week_dates(b)
        dat = get_rota_data(b) 
        evnt = get_events(b)
        rsd = get_rotaSec(b)
        lrd = get_leader_rota(b)
        lsr = get_leader_support(b)
        chs = CHS.getState(chFile,'chState')
        newsDat=get_news(b)
        del newsDat[0]  # delete the first [
        #print(newsDat[0])
        if chs=="OK_ON":
            heat_on=True
        elif chs=="OK_OFF":
            heat_on=False
        else:
            heat_on=None  # probably off line       
        return render_template("table31.html",headings=head,events=evnt,rotaSecs=rsd, leadRota=lrd, leaderSupport=lsr, data=dat, newsdata=newsDat, weekStart = weekStart,weekEnd=weekEnd,heat_on=heat_on)


if __name__ == '__main__':
    #logging.basicConfig(filename='sb156.log', encoding='utf-8', level=logging.DEBUG)
    TEMPLATES_AUTO_RELOAD = True
    app.run(debug=False)


