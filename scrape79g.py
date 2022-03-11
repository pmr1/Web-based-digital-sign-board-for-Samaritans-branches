"""
python 3
This extracts overall data about the rota and news items
The files extract are located on https://www.3r.org.uk/api  you must have a registered account to access this
It does not determine whether the voluntee has confirmed that shift
That can be found in shift.json

in tuple order
header + day date  monday 26 Apr 2021, Tuesday 27 Apr 2021  etc
event1
event2
rota name eg sec, leader support, kirkcaldy rota
each row thereafter are the volunteer shfits
extract started 1/5/21
need to add start and enddates for extraction
times sorted in order hopefully
  this is more difficult since times are structured '08:00 - 17:00'
  part of this method could be
  from datetime import datetime
        my_dates = ['5-Nov-18', '25-Mar-17', '1-Nov-18', '7-Mar-17']
        my_dates.sort(key=lambda date: datetime.strptime(date, "%d-%b-%y"))
        print(my_dates)
    strip out All-Day events and put in a seperate list
    then see testSort1.py in Dropbox\Samaritans ...
Headers
   rota sec
   leader support
   leaders
   events
   news
   
confirmed marked as '1'
column shifts by day
This generates shift rota correctly using dummy data
still add Rota sec row
Leader support row
better formating
Only event name store
shed unwanted functions merge rota sec with leader support
get live data  now includes '[sign up]' x2 for no volunteers available
extract shiftimes for central heating control
This extracts where requested week data once a week
rota data once an hour along with central heating data
this run every hour but only events get update every week
copes with run scrape mid week
added exception handling on request
added file locking
undated writeCfg
using alternate buffers  A and B

dependacies
python
  json
  atetime import *; from dateutil.relativedelta import *
  config
  calendar
  dateutil.parser
  ateutil.parser import parse
  requests
  pickle
this repo
  readChStateM16
  writeCfg35M
  htmlstrip3m
  
  external files  used and modified
  cHconfig.cfg  
  
  generates text files used but web page to generate
    1.  Rota data table  specific to the Samaritans branch
    	events, leadersRota, leadersSupport, newsData,rotaSec,weekDates,centralHeat with suffix .txt
    	
    2.  Rollng news of the day
    3.  24 hour timing schedule to control a central heating system
 
  
"""
ver = 'scrape79.py 280222'
import json
from datetime import *; from dateutil.relativedelta import *
import config
import calendar
import dateutil.parser
from dateutil.parser import parse
import requests
import readChStateM16 as CHS
import writeCfg35M as WC
import pickle
import htmlstrip3m


APIKEY = 'APIKEY your api key here'

chFile ='cHconfig.cfg'


def get_data(dstart,dend,dataType):
    # dataType 1 for shift data  , 2 for rota data , 3 for event data
    if dataType == 1:
        try:
            shiftData = requests.get("https://www.3r.org.uk/shift.json?start_date="+dstart+"&end_date="+dend, headers={"Authorization": APIKEY})
            shift = json.loads(shiftData.content)
            return shift
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
               
    if dataType == 2:
        try:
            rotaData =requests.get("https://www.3r.org.uk/stats/export_rotas.json?start_date="+dstart+"&end_date="+dend, headers = {"Authorization": APIKEY})
            rota = json.loads(rotaData.content)
            return rota
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
    if dataType == 3:
        try:
            eventData = requests.get("https://www.3r.org.uk/events.json", headers={"Authorization": APIKEY})
            events = json.loads(eventData.content)
            return events
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    if dataType == 4:
        try:
            eventData = requests.get("https://www.3r.org.uk/news.json", headers={"Authorization": APIKEY})
            events = json.loads(eventData.content)
            return events
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

def getNextEvents():
    # run from the day it is requested on and n days in advance
    eventData = requests.get("https://www.3r.org.uk/events.json", headers={"Authorization": APIKEY})
    events = json.loads(eventData.content)
    return events
       
    
def dataStore(fileN, data):
    json_formated_str = json.dumps(data, indent=4)
    fn = open(fileN,"w")
    fn.write(json_formated_str)
    fn.close()

    



def listDates(offset):
    # expect rowdata in form of list or tuple
    # and date format is year-month-day
    # offset from current date + or -
    TODAY = date.today()
    NOW=datetime.now()
    row=[]; rowH=[]; weekD =[]
    #dtr = TODAY+relativedelta(weekday =MO(+1))  # starting next monday
    dtr = TODAY+relativedelta(weekday =MO(offset) )  # starting offset monday
    if TODAY < dtr:
        dtr = TODAY+relativedelta(weekday =MO(offset-1))
    for i in range(7):
        dt =dtr+relativedelta(weekday=i)  # dt is a tuple
        #d= str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
        dh = dt.strftime("%d %B %Y")
        rowH.append(dh)
        d=dt.strftime("%Y-%m-%d")
        row.append(d)
    dtr1 = TODAY+relativedelta(weekday =MO(offset+2) )
    # the offset depends on the weekday if < 1( ie monday) offset is +2
   # ele its +1
    if date.today().weekday() <1:
    	monNext = TODAY + relativedelta(weekday =MO(offset+2))
    else:
        monNext = TODAY + relativedelta(weekday =MO(offset+1))
    return row,rowH,monNext

def get_events(E,endDate, weekDates):
    # capture the week of events
    row=[]
    for i in range(8):
         row.append('')
    #i=0
    
    for event in E['events']:
      for j in range(6):
        #print(event['date'])
        if parse(event['date']) <= parse(endDate):
            #print(event['date'])
            for i in range(6):
                if event['date'] == weekDates[j] :
                    #rw = event['name'] +" "+ event['description'] # +" "+event['date']
                    rw = event['name'] # +" "+event['date']
                    row[j+1] = rw
    return row

def Convert(lst):
    # cf https://www.geeksforgeeks.org/python-convert-a-list-to-dictionary/
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def detWeekDay(weekDates, d):
    # determine week day
    dd = d.strftime('%Y-%m-%d')
    i = 0
    #print (dd)
    stop = False
    while (dd != weekDates[i]) and not stop:
        i = i + 1
        if i > 6:
            stop = True
            return 0
    return i
                     
                  
def get_shift_times_row(stime,weekDates,rw):
    row=[]
    chtimes=''
    for i in range(8):   # initialise row for each time session
            row.append('')
    ri =0

    t=parse(stime[rw]['start_datetime'])
    ri = detWeekDay(weekDates, t)
    dtime = stime[rw]['duration']/ 3600
    if dtime < 24:    
       rowText =t.strftime("%Y-%m-%d ")+t.strftime('%H:%M') + ' - '+ str(int((t.hour+dtime) % 24)) + ':' + str(t.minute)
       # retreive central heating start and finish times start time is 15 before rota starts
       #print(t.hour)
       chtimes = t.strftime("%Y-%m-%d")+' '+str((t.hour-1)%24)+':'+str(t.minute+45)+"-"+ str(int((t.hour+dtime) % 24)) + ':' + str(t.minute)      
    else:
        if stime[rw]['rota']['name'] == 'Leaders Rota':
           rowText = 'All Day'
        elif stime[rw]['rota']['name'] == 'Leader Support':   
           rowText ='All Week' # + stime['rota']['name']
        else:
            rowText ='All Day'
    row[0] = rowText
    ri = ri +1
    row[ri] = stime[rw]['rota']['name']+'|'  # rota type ie sec, leader or Kirkcald Rota
    k = 0
    if stime[rw]['volunteer_shifts'] == [] and stime[rw]['num_volunteers_satisfying'] == 0:
        row[ri] = row[ri] +' '+  '[sign up]' +' '+  '[sign up]'
        #print(row[ri])
    else:         
        for vs in stime[rw]['volunteer_shifts']:  # this makes it into a dictionary
            k = k +1  # number of passes or volunteers
            s =  parse(stime[rw]['start_datetime'])      
            t = s.strftime('%Y-%m-%d')
            vn =''
               #print('date ',t)
            vsDict = vs  #v[0]  # make it a dictionary
           #print(vsDict)
            vn = vsDict['volunteer']['name']
            #print('vn ',vn)      
            confirm = vsDict['confirmed_at']
            if confirm != None:
               volName = vn  + '' # confirmed'
            else:
               volName = vn + ''
            if stime[rw]['satisfied']:
                row[ri] = row[ri] +' '+ volName
                #print(" sats ", row[ri])
            else:
                if stime[rw]['num_volunteers_filling'] == 2:
                  if k == 2:
                      row[ri] = row[ri] +' '+ volName + '[sign up]'
                      
                  else:
                      row[ri] = row[ri] +' '+ volName   
                      row[ri] = row[ri] +' '+  '[sign up]'
                if stime[rw]['closed_at'] != None:
                    if k==1:      
                        row[ri] = volName +' '+ '[closed]'                          
    return row, chtimes

def compress(L):   # compress into one row of weekdays 
    cList=[]
    j =0
    #print('l',len(L))
    while j < len(L):
        tod = L[j][0]  # time of day but they on different dates
        #print ('t ', tod)
        #print(tod)
        #tod.parse(str(tod)) ; print(tod.strftime('%H:%M'))
        # It is assumbed they are in time order
        end= False
        rowText =[]
        k=0;
        for i in range(8):
            rowText.append('')
        tt = tod.split(" ")[1]    
        t = L[k][0].split(" ")[1]
        #print(j,tt)
        while not end:  # conditions processed from left to right
            t = L[k][0].split(" ")[1]
            if t==tt:
                #print(k,t)
                for i in range(8):
                    if L[k][i] != '':
                       rowText[i] = L[k][i]
                       #print(rowText[i])
            
            end =(k==len(L)-1)
            cList.append(rowText)
            k = k+1
        j += 1
    
    return cList                         
               
# now weed out duplicates
# see https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
# for non hassable lists
    seen = {}
    dupes =[]
    no_dupes = [x for n, x in enumerate(cList) if x not in cList[:n]]       
    return no_dupes




def sortMethod(e):
    return int(e)

def rowTimeSort(listOfTimes):
    fn=open("listOfTimes.txt","w")
    for i in range(len(listOfTimes)):
        fn.write(str(listOfTimes[i])+'\n')
    fn.close()
    sortThem=[]
    for i in range(len(listOfTimes)):
      if listOfTimes[i][0] =='All Day' or  listOfTimes[i][0] =='All Week':
          t= parse('00:00')
          sortThem.append(str((t.hour *60) + t.minute))
      else:
          fd = str(listOfTimes[i][0]).split(" ")        
          thour = int(str(fd[1]).split(':')[0])
          tmin = int(str(fd[1]).split(':')[1])
          sortThem.append(str(thour*60+tmin)) 
    sortThem.sort(key=sortMethod) # a string of numberical value sort
    
    newList =[]
    for i in range(len(sortThem)):      
        m=0
        # now search over all times
        for j in range(len(listOfTimes)):
            if listOfTimes[j][0] == 'All Day' or  listOfTimes[j][0] =='All Week':
                t= parse('00:00')
                if str((t.hour *60) + t.minute)==sortThem[i]:
                    newList.append(listOfTimes[j])
            else:
                #fd = listOfTimes[j][0].split('-')[0]
                fd = str(listOfTimes[j][0]).split(" ")        
                thour = int(str(fd[1]).split(':')[0])
                tmin = int(str(fd[1]).split(':')[1])
                if str((thour *60) + tmin)==sortThem[i]:
                    newList.append(listOfTimes[j])
                
    # remove duplicates
    no_dupes = [x for n, x in enumerate(newList) if x not in newList[:n]]       
                    
    # now need to combine the common all week dates for the same time
    printData("preDupes.txt", no_dupes, False)
    #with open('no_dupes.bin','wb') as fp:
     #   pickle.dump(no_dupes,fp)
    nextList = compress(no_dupes)#  not required
    #printData("postComp.txt",nextList, False)
    no_dupes = [x for n, x in enumerate(nextList) if x not in nextList[:n]]
    printData("postComp.txt",no_dupes, False)
    return no_dupes

    
        
def printData(fileName, L, oneList):
    fn=open(fileName,"w")
    if oneList:
        fn.write(str(tuple(L)))
    else:
        for i in range ( len(L)):
            fn.write(str(L[i])+'\n')
    fn.close()

def convertToRows(L, weekDates):
    # takes list L and generates a row list of RL[0] is the session time RL[weekDay between 0 - 6] is the date RL1..n]
    # needs work !!!!!!
    rw=rows=[]
     # L has lists already in date order and there is a row for each time  These rows will have to be sorted in time order
     # rw has items: time of day, day1, day2, day3,day4. day5, day6, day7
     # lastly these rows have to be sorted in time order
    
    for c in range(len(L)):
        tod =L[c][0][0]  # eg 08:00 - 11:0
        dr = L[c]
        #print(tod,dr)
        for i in range(8):
            rw.append('')
        rw[0]=tod
        i =1
        #for each weekdate but L is in date order
        while i < 8:
            rw[i] = str(L[i-1][1][1]) + str(L[i-1][2])
            for j in range(len(dr)):
                for k in range(len(dr[j])):
                    rw[j] = rw[j]+dr[j][k]
            i = i+1
        rows.append(rw)
    return rows
        
       
def extract(bf):
    print(ver)
    weekDates, weekH, dayBeyond=listDates(0)   # this week
    #print(weekDates[0], weekDates[6], dayBeyond, weekH)

    printData(indexDir+bf+'weekDates.txt',weekH, True)

    shiftData = get_data(str(weekDates[0]),str(dayBeyond),1)
    if shiftData =="no connection":
        return shiftData
    rota = get_data(str(weekDates[0]),str(dayBeyond),2)
    NOW=datetime.now()
    dt = NOW.strftime("%Y-%m-%d")
    # next weeks events else use previous events on Sundays at 00:00 - 01:00 or less
    events =get_data(str(weekDates[0]),str(dayBeyond),3)
    if weekDates[6] == dt and NOW.hour < 1 :
        events =get_data(str(weekDates[0]),str(dayBeyond),3)
    # declare data tables 
    fn = open(indexDir+bf+"tableData.txt","w")  # volunteer shifts
    fnlr = open (indexDir+bf+"leadersRota.txt","w")
    fnls = open (indexDir+bf+"leadersSupport.txt","w")
    fnrs = open (indexDir+bf+"rotaSec.txt","w")
    fnev = open (indexDir+bf+"events.txt","w")
    fcht = open (indexDir+"centralHeat.txt","w")  # central heating control data
    

    stime = shiftData['shifts']
    rowData =[]; leaderRota = [] ; chData=[]
    for row in range (len(stime)):
        shiftRow, cht = get_shift_times_row(stime,weekDates,row)
        if str(shiftRow).find('Rota Secs')>0:   # only one per week
            fnrs.write(str(tuple(shiftRow))+'\n')
        elif str(shiftRow).find('Leader Support')>0 : # only one per week
            fnls.write(str(tuple(shiftRow))+'\n')
        elif str(shiftRow).find('Leaders Rota') >0 :  # only one per day
            #fnlr.write(str(tuple(shiftRow))+'\n')
            leaderRota.append(shiftRow)
        #elif str(shiftRow).find('Kirkcaldy Rota') >0:  
        else:
            rowData.append(shiftRow)  # volunteer shifts
            # collect central heating control times
            chData.append(cht)
            #fn.write(str(tuple(shiftRow))+'\n')
    #print(leaderRota)
    sortedRota = rowTimeSort(leaderRota)   # Flag2 there are two leadersRota rows one is timed 08:00 - 2:0
    
    printData("lrota.txt",sortedRota, False)
    
    # now right the anomaly  8:0 - 02:0  *********
    an = sortedRota[1][0]
    # strip out the date
    ant = str(an).split(" ")
    
    adj = ant[1]+ant[2] +ant[3]
    sortedRota[1][0] = adj
    leadRota = sortedRota
    for item in leadRota:
        fnlr.write(str(tuple(item))+'\n')

    sortedTimes = rowTimeSort(rowData)
    #save ch times
    fcht.write(str(tuple(chData)))

    #for i in range(len(chData)):
    #    print(str(chData[i]))

    #print("ch epochs ", len(chData))

    for i in range(len(sortedTimes)):
        # strip out data data
        tod = sortedTimes[i][0]
        t = tod.split(" ")
        #print(tod)
        sortedTimes[i][0] = t[1]+t[2]+t[3]
        fn.write(str(tuple(sortedTimes[i]))+'\n')
        
    fn.close()
    fnlr.close()
    fnls.close()
    fnrs.close()
    fcht.close()

    #print(sortedTimes)
    # weekDates redetermined because events start from present date
    weekDates, weekH, dayBeyond=listDates(0)
    print("event dates ",weekDates[0],dayBeyond)
    #events = getNextEvents()
    #dataStore('eventsNext.txt',events)
    print('events') 
    dataStore('eventsNext.txt',events)
    for i in range(len(events)):
        eventRow= get_events(events,weekDates[6], weekDates)
        eR = str(tuple(eventRow))
        ER = remove_non_ascii(eR) 
        fnev.write(ER)
    # print(tuple(eventRow))
    fnev.close()
    return "done"
def  remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) < 0x0080)


def extractNews(dd,buf):
    # fn has to be json formated file
    #nd = open (fn,'r')
    fnn = dd+buf + 'newsData.txt'
    fnnd = open (fnn,'wb') # output
    #json_data = nd.read()  
    #news = json.loads(json_data)
    news = get_data('','',4)
    #nd.close()
    nitems = news['news_items']
    newsItems=[]
    newsCount =0
    for new in news['news_items']:
        #print(new)
        who = new['creator']['name']
        tle = new['title']
        newsDate = new['created_at']
        #tt.strftime("%Y-%m-%d ")
        nd=parse(newsDate).strftime("%d-%m-%y ")
        #print('news date' , nd)
        nI = new['body']
        nIm = htmlstrip3m.strip_tags(nI)
        tt2= str(nIm).replace('\u200b','')
        tt2 = tt2.replace('\r\n','')
        tt2 = tt2.replace('\xa0','')
        tt2 = tt2.replace("'",'')
        tt2 = remove_non_ascii(tt2) 
        #print('item', newsItem)
        ni = str('$$')+str(who)+'|'+ str(tle)+'|'+str(nd)+'|'+str(tt2)
        newsItems.append(ni)
        newsCount += 1
        if newsCount % 2 == 0:
          nd = str(newsItems) +  str('\r')
          sw = str(nd).encode('utf-8') 
          fnnd.write(sw)
          newsItems = []
    fnnd.close()
    return fnn
     

def makeFlat(l):
    # take rows of list l and arange in one in
    # line is expected to be in week day order
    rl =[]
    for i in range(8):
        rl.append('')
    rl[0] = l[0][0]  #  'All Day'
    for i in range(6):
        rl[i+2] = l[i][i+2]  # rl is rota leader for that day
    return rl
    
#indexDir ='/home/samsvol/indexPages/'
indexDir ='/home/becky1/indexPages/'
#indexDir =''
# flag data being changed
b = CHS.getState(chFile,'buffer')
# print(b)
sw = (b=='A')
if sw:  # the one in use by web page
    bf ='buffer:'"'B'"
    b='B'
else:
    bf ='buffer:'"'A'"
    b='A'
# print(sw,b)
#WC.writeConfig(chfile,bf)
NewsFile = extractNews(indexDir,b)
print('news data saved to ', NewsFile)
result = extract(b)
NOW=datetime.now()
sdate = NOW.strftime("%Y-%m-%d")
stime = NOW.strftime('%H:%M')
print(result,sdate, stime)
#flag now its safe to read this buffer
WC.writeConfig(chFile,bf)


 
 
