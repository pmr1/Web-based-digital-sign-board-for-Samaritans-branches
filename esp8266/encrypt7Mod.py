'''
simple encryption of ascii data
see code4.xlsx check for duplicates
module use
only returns and uses ascii messages
this does not require the search start position to be passed because it searches
for the predefined start character
'''

ver =' encrypt7mod.py 170621'

def genSequence(taps):
    global gcode
   # generalised 8 bit sequence generator.  LFSR taps given by taps
   # t1=t2=t3=t4=t5=t6=t7=t8=b=0
    t1 = taps & 1 & (gcode & 0x00FF)
    t2 = (taps & 2 & (gcode & 0x00FF)) >> 1
    t3 = (taps & 4 & (gcode &0x00FF)) >> 2
    t4 = (taps & 8 & (gcode &0x00FF)) >> 3
    t5 =(taps & 0x10 & (gcode &0x00FF)) >> 4
    t6 =(taps & 0x20 & (gcode &0x00FF)) >> 5
    t7 =(taps & 0x40 & (gcode &0x00FF)) >> 6
    t8 =(taps & 0x80 & (gcode &0x00FF)) >> 7
    # apply feeback taps
    b = t1 ^t2 ^t3 ^ t4 ^ t5 ^ t6 ^ t7 ^ t8
    # rotate code
    gcode = (gcode & 0x00FF) << 1
    gcode =  (gcode & 0x00FF) | b
    return (b & 1 )
    

def codeStart(cs):
    global gcode
    gcode = cs  #code start point
    
def setFeedBack(fbt):
    global FBT
    FBT = fbt

def check(c):
    global SCHAR
    SCHAR = ord(c)
     


def encryptMesg(pTm,cs):
    # pTm plain text message
    # cTm cyphertext message
    # fbt feedback taps
    global FBT
    b=1 ; cTm =[] ; feedBackTaps = FBT
    codeStart(cs)
    for i in range(len (pTm)):
        b = genSequence(feedBackTaps)
        cTm.append((gcode & 0x00FF) ^ord(pTm[i]))
        encryptM =''
        for i in range(len (cTm)):
            encryptM = encryptM + chr(cTm[i])
    return encryptM


def decryptMesg(cTm,cs):
    #cTm cyptertext message
    #cs code start
    global gcode, FBT
    b=1 ; feedBackTaps = FBT
    codeStart(cs)
    pTm =[]
    for i in range(len (cTm)):
        b = genSequence(feedBackTaps)
        pTm.append((gcode & 0x00FF) ^ord(cTm[i]))
    message =''
    for i in range(len (pTm)):
        message = message + chr(pTm[i])
    return message




def findMesg(ctm):
    # rotates gcode to find start position and
    # returns the decrypted message
    global gcode, FBT, SCHAR
    b=1 ; feedBackTaps = FBT 
    cs = 1
    cTm =[]
    codeStart(1)
    b=1    
    test = ord(ctm[0])  
    stop = False
    i=1; cs = 1
    while not stop:
        codeStart(i)
        b = genSequence(feedBackTaps)
        if test ^ (gcode & 0x00FF) == SCHAR:
           cs =i
           stop = True
        i +=1
    # can't shorten message because sequence would not match
    print('start',test,cs)
    pTm= decryptMesg(ctm ,cs)         
    return pTm 
    




    



