# Simplified version of Nokia Data Logger.
# This program just stores multiple screenshots at user-defined time
# intervals. Images can then be transferred to PC for further processing.


import e32db,time
from appuifw import *
import appuifw
from graphics import *
import graphics
import e32
import keycapture
from key_codes import *


timelaps = 10 #seconds

def cb_capture(key):
    global offset, HWidth, VWidth, HHeight, VHeight, num,PixThreshold, img , Xstart, Ystart,  HSegOn, VSegOn, HSegOff, VSegOff, fg , threshold,TotColorR,TotColorG,TotColorB
    img = graphics.screenshot()
    
    if key==keycapture.EKeyYes:
        note(u'Captured YES key!',u'info',1)
        fg.unset()
    if key==keycapture.EKeyNo:
        note(u'Captured no key!',u'info',1)
 

def Reader():
   global canvas, PixThreshold, HWidth, VWidth, HHeight, VHeightm,  fg, img, threshold, over, TopLeftX, TopLeftY, filecount
   img=graphics.screenshot() # Take screenshot
   #filenum = Lead0(filecount)
   t = repr(e32db.format_time(time.time()))
   timestamp = t[8:12] + t[5:7] + t[2:4] + "_" + t[13:15] + t[16:18] + t[19:21]
   img.save("e:\\nokia\\images\\LCD" + timestamp + ".jpg")
   print "e:\\nokia\\images\\LCD" + timestamp + ".jpg"

            
def Adjust():
  global offset, HWidth, VWidth, HHeight, VHeight, num,PixThreshold, img, filecount
# create a loop to get stuff handled that needs to be done again and again
  running = 1
  switch = 1
  filecount = 0
  while running:
      if switch == 1:
          filecount = filecount + 1
          Reader()
          e32.ao_sleep(timelaps)
      e32.ao_yield()
          

def quit():
    global running
    running=0
    appuifw.app.set_exit()

app.exit_key_handler = quit
capturer=keycapture.KeyCapturer(cb_capture)
capturer.forwarding=0
capturer.keys=(
               keycapture.EKeyYes,
               keycapture.EKeyNo,
               )
capturer.start()

Adjust()

script_lock = e32.Ao_lock()
script_lock.wait()



        


 


