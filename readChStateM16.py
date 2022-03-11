'''
it can read the full cHconfig.cfg which has the form
   chState:'OK_ON',temp:'34', setTemp:'33',fileState:'unlocked' , buffer:'A'  or 'B'
and returns the requested state
read different config data 

'''
ver= 'readChStateM16.py 060122'
import config
dataDir ='/home/paulmr/indexPages/'
# this returns the chState from remoteControl41
def getState(cf,what):
    try:
      cffile = dataDir+cf
      cfg = config.Config(cffile)  # this has to be loaded each time
      if what == 'chState':
          return cfg['chState']
      elif what == 'temp':
          return cfg['temp']
      elif what == 'setTemp':
          return cfg['setTemp']
      elif what == 'fileState':
          return cfg['fileState']
      elif what == 'buffer':
          return cfg['buffer']       
      else:
          return 'no data'
    except: KeyError('no data')  # required if no data in chConfig.cfg
    
    

