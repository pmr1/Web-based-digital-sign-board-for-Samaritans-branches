'''
resides in www/FlaskApps directory
run in samsvol
cHconfig.cfg to be in this form
chState:'OK_ON',temp:'34',fileState:'unlocked'
choice of config files
it needs to be in the form  eg fn.write('chState:'+ "'"+data+"'")
and returns new setting in cHconfig.cfg
'''
ver ='writeCfg35M.py 060122'

cfgDir ='/home/samsvol/indexPages/'
def writeConfig(cf,data):
    try:
        fn=open(cfgDir+cf,'r')
        Cfg=fn.readline()
        fn.close()
        currentData = Cfg.split(',')
        #print(currentData, len(currentData))
        state = True
    except OSError:
        currentData = "no data"
        state = False
    #print (chS)
    if state:
        
        i= 0
        for cd in currentData:
            if cd.split(':')[0]==data.split(':')[0]:
                break
            i+=1
             
        #print(cd,i)
        currentData[i] = data
        #print(currentData)
        fn=open(cfgDir+cf,'w')
        for i in range(len(currentData)):
            if i < len(currentData)-1:
                fn.write(currentData[i]+',')
            else:
                #print(i)
                fn.write(currentData[i])
        fn.close()
        return (currentData)
    else:
        return(currentData)

    
