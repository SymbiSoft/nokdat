# Up/down arrows change figure size;
# 5: save settings to file;
# 0: load settings from file;
# 1-3: change distance among figures;
# 4-6: change segments size;
# 7-9: change black/white threshold

import keycapture

import fgimage
from appuifw import *
from graphics import *
#import camera
import e32
from key_codes import *
import appuifw
#from camera import *
import miso # Needed for backlight refresh
import graphics
import keypress

PixThreshold = 66
TopLeftX = [ 30, 65, 65,  30,  20, 20, 30]
TopLeftY = [ 60, 75,120,150,120, 75, 105]

Figures=[[1,1,1,1,1,1,0], \
         [0,1,1,0,0,0,0], \
         [1,1,0,1,1,0,1], \
         [1,1,1,1,0,0,1], \
         [0,1,1,0,0,1,1], \
         [1,0,1,1,0,1,1], \
         [1,0,1,1,1,1,1], \
         [1,1,1,0,0,0,0], \
         [1,1,1,1,1,1,1], \
         [1,1,1,1,0,1,1]]


def cb_capture(key):
    global offset, HWidth, VWidth, HHeight, VHeight, num,PixThreshold, img , Xstart, Ystart,  HSegOn, VSegOn, HSegOff, VSegOff, fg , threshold,TotColorR,TotColorG,TotColorB, switch
    x=8
    y=10  
    XINC = 1
    XINC2 = 2
    YINC = 1
    YINC2 = 2
    YINC3 =4
    YINC4 = 4
    OFFSETINC = 10
    THRESHINC = 1000

    offset = 70
    num=[0,offset,2*offset,3*offset,4*offset,5*offset] 
 
  
    fg = fgimage.FGImage()
    img = graphics.screenshot()
    
    if key==keycapture.EKeyYes:
        note(u'Captured YES key!',u'info',1)
        fg.unset()
    if key==keycapture.EKeyNo:
        note(u'Captured no key!',u'info',1)

    if key==keycapture.EKey2:
      switch = 2
    if key==keycapture.EKey5:
      switch = 1
      

       
    # Tune figures distance.
    if key==keycapture.EKey1:
          offset = offset - OFFSETINC
          num=[0,offset,2*offset,3*offset,4*offset,5*offset] 
    if key==keycapture.EKey3:
          offset = offset + OFFSETINC
          num=[0,offset,2*offset,3*offset,4*offset,5*offset] 
          
          
    # Tune segments width    
    if key==keycapture.EKey4:
          HHeight = HHeight - 1
          over.clear()
    if key==keycapture.EKey6:
          HHeight = HHeight + 1
          over.clear()

                  
    #Tune threshold                  
    if key==keycapture.EKey7:
        threshold = threshold - THRESHINC
        over.clear()
        print threshold
    if key==keycapture.EKey9:
        threshold = threshold + THRESHINC
        print threshold
        over.clear()
        
    # Resize figures: only position of lower segment is changed, others
    # positions/sizes depend on it.
    if key==keycapture.EKeyStar:
          TopLeftY[3] = TopLeftY[3]- YINC4
          over.clear()          
    if key==keycapture.EKeyHash:
          TopLeftY[3] = TopLeftY[3]+ YINC4
          over.clear()

    # Save settings     
    if key==keycapture.EKey0:
        filename=u'c:\\LCD.ini'
        out_file = open(filename,"w")
        out_file.write("Offset=" + repr(offset) + "\n")
        out_file.write("Threshold=" + repr(threshold) + "\n")
        out_file.write("Thickness=" + repr(HHeight) + "\n")   
        for i in range(7):
          out_file.write("TopLeftX[" + repr(i) + "]=" + repr(TopLeftX[i])+"\n")     
          out_file.write("TopLeftY[" + repr(i) + "]=" + repr(TopLeftY[i])+"\n")     
        out_file.close()

          
# Determine figure size from bottom segment position:
    TopLeftY[6] = (TopLeftY[3] + TopLeftY[0])/2
    TopLeftY[1] = TopLeftY[0]+ HHeight
    TopLeftY[2] = TopLeftY[6]+ HHeight
    TopLeftY[4] = TopLeftY[2]
    TopLeftY[5] = TopLeftY[1]
    TopLeftX[1]=TopLeftX[5]+VWidth+HWidth
    TopLeftX[2]=TopLeftX[1]
    VHeight = TopLeftY[6] - (TopLeftY[0]+HHeight)
    HWidth = VHeight
    VWidth = HHeight


def InitVars():
  global offset, threshold, HWidth, VWidth, HHeight, VHeight, num, HSegOn, VSegOn, HSegOff, VSegOff, fg, over,TotColorR,TotColorG,TotColorB,adjust_image, Xstart, Ystart
  offset = 70
  num=[0,offset,2*offset,3*offset,4*offset,5*offset] 
  HHeight = 10
  VWidth = HHeight
  VHeight = TopLeftY[6] - (TopLeftY[0]+HHeight)
  HWidth = VHeight
  TopLeftY[6] = (TopLeftY[3] + TopLeftY[0])/2
  TopLeftY[1] = TopLeftY[0]+ HHeight
  TopLeftY[2] = TopLeftY[6]+ HHeight
  TopLeftY[4] = TopLeftY[2]
  TopLeftY[5] = TopLeftY[1]
  TopLeftX[1]=TopLeftX[5]+VWidth+HWidth
  TopLeftX[2]=TopLeftX[1]
  threshold=200*HWidth*HHeight
  
  fg = fgimage.FGImage()
  over = Image.new((176,180))
  
  Xstart = num[0]+TopLeftX[0]-VWidth
  Ystart = TopLeftY[0]
  Xend = num[0]+TopLeftX[0]+HWidth+VWidth
  Yend = TopLeftY[3]+HHeight   
  adjust_image = Image.new((Xend-Xstart,Yend-Ystart))
  
  

def Adjust():
   global canvas, PixThreshold, HWidth, VWidth, HHeight, VHeight,  fg, img, threshold, over, TopLeftX, TopLeftY, Xstart, Ystart,adjust_image
   Xstart = num[0]+TopLeftX[0]-VWidth
   Ystart = TopLeftY[0]
   Xend = num[0]+TopLeftX[0]+HWidth+VHeight
   Yend = TopLeftY[3]+HHeight   
   adjust_image = adjust_image.resize((Xend-Xstart,Yend-Ystart))
   for n in range(1): # Loop through various figures
    miso.reset_inactivity_time() # Keep light on
    fg.set(Xstart, Ystart, adjust_image._bitmapapi())    
    
    
    
def Reader():
   global canvas, PixThreshold, HWidth, VWidth, HHeight, VHeight,  fg, img, threshold, over, TopLeftX, TopLeftY
   TotColorR = 0
   TotColorG = 0
   TotColorB = 0
   x = 0
   y = 0
   n = 0
   #fg.unset() # Remove overdrawing before examining screen.
   img=graphics.screenshot() # Take screenshot
   for n in range(1): # Loop through various figures
    miso.reset_inactivity_time() # Keep light on
    # Keep camera on by simulating keypress:
    #keypress.simulate_key(EKeyDownArrow,EKeyDownArrow)
    # Cancel keypress effect:
    #keypress.simulate_key(EKeyUpArrow,EKeyUpArrow)
    
    idx = 0
    aa =0
    bb=0
    segm=[9,9,9,9,9,9,9] # Initialize segments to "8" (1=on=black, 2=off=transparent)
    for idx in range(7): # Loop through segments.
        TotColorR = 0 # Per each segment calculate a separate sum.
        TotColorG = 0
        TotColorB = 0   
          
        # Neighbours colors - horizontal:   
        TotColorRhl = 0 
        TotColorGhl = 0
        TotColorBhl = 0     
           
        TotColorRhu = 0 
        TotColorGhu = 0
        TotColorBhu = 0      
          
        # Neighbours colors -  vertical:   
        TotColorRvr = 0 
        TotColorGvr = 0
        TotColorBvr = 0     
           
        TotColorRvl = 0 
        TotColorGvl = 0
        TotColorBvl = 0      
          
        # Examine a box inside the segment; values of each pixel are summed up into
        # a single value,which is the compared to a threshold to determine if
        # the segment is on (=black=under threshold) or off (=white=over threshold).
        if (idx == 0) or (idx == 6) or (idx == 3): # Horizontal segments
          Xstart = num[n]+TopLeftX[idx]
          Xend = num[n]+TopLeftX[idx]+HWidth
          Ystart = TopLeftY[idx]
          Yend = TopLeftY[idx]+HHeight   
        else: # Vertical segments
          Xstart = num[n]+TopLeftX[idx]
          Xend = num[n]+TopLeftX[idx]+VWidth
          Ystart = TopLeftY[idx]
          Yend = TopLeftY[idx]+VHeight         
        #print "idx=",idx,":",Xstart, Ystart              
        for x in range(Xstart, Xend): # sum up color of each pixel of the segment:
          for y in range(Ystart, Yend):
            tempR, tempG, tempB =  img.getpixel((x,y))[0]
            TotColorR = TotColorR + tempR
            TotColorG = TotColorG + tempG
            TotColorB = TotColorB + tempB 
        if (idx == 0) or (idx == 6) or (idx == 3): # Horizontal segments neighbours
          for x in range(Xstart, Xend): # Horizontal segment lower neighbour
            for y in range(Ystart+HHeight, Yend+HHeight):
              tempR, tempG, tempB =  img.getpixel((x,y))[0]
              TotColorRhl = TotColorRhl + tempR
              TotColorGhl = TotColorGhl + tempG
              TotColorBhl = TotColorBhl + tempB 
          for x in range(Xstart, Xend): # Horizontal segment upper neighbour
            for y in range(Ystart-HHeight, Yend-HHeight):
              tempR, tempG, tempB =  img.getpixel((x,y))[0]
              TotColorRhu = TotColorRhu + tempR
              TotColorGhu = TotColorGhu + tempG
              TotColorBhu = TotColorBhu + tempB 
        else: # Vertical segments neighbours
          for x in range(Xstart+VWidth, Xend+VWidth): # Vertical segment right neighbour
            for y in range(Ystart, Yend):
              tempR, tempG, tempB =  img.getpixel((x,y))[0]
              TotColorRvr = TotColorRvr + tempR
              TotColorGvr = TotColorGvr + tempG
              TotColorBvr = TotColorBvr + tempB 
          for x in range(Xstart-VWidth, Xend-VWidth): # Vertical segment left neighbour
            for y in range(Ystart-HHeight, Yend-HHeight):
              tempR, tempG, tempB =  img.getpixel((x,y))[0]
              TotColorRvl = TotColorRvl + tempR
              TotColorGvl = TotColorGvl + tempG
              TotColorBvl = TotColorBvl + tempB 
            #if tempR+tempG+tempB > PixThreshold:
              #over.point((x,y),65000)
            #else:
              #over.point((x,y),10000)
        #print idx,TotColorR + TotColorG + TotColorB, threshold
        if TotColorR+TotColorG+TotColorB > threshold: # If white, then off.
        #   print "white" 
           if (idx == 0) or (idx == 6) or (idx == 3): # Horizontal segments
            over.rectangle((Xstart,Ystart,Xstart+HWidth,Ystart+HHeight),0x000000,0xaaaaaa) 
           else:
            over.rectangle((Xstart,Ystart,Xstart+VWidth,Ystart+VHeight),0x000000,0xaaaaaa) 
           segm[idx]=0
        else:
          # print "black"
           if (idx == 0) or (idx == 6) or (idx == 3): 
             over.rectangle((Xstart,Ystart,Xstart+HWidth,Ystart+HHeight),0x000000,0x333333) 
           else:
             over.rectangle((Xstart,Ystart,Xstart+VWidth,Ystart+VHeight),0x000000,0x333333)            
           segm[idx]=1
        if (idx == 0) or (idx == 6) or (idx == 3):           
          out_file.write("Up,Mid,Down " + repr(idx) + "=" + chr(9) + \
          repr(TotColorRhu+TotColorGhu+TotColorBhu) + "," + chr(9) + \
          repr(TotColorR+TotColorG+TotColorB) +  "," + chr(9) + \
          repr(TotColorRhl+TotColorGhl+TotColorBhl)+ \
          "("+repr(TotColorR+TotColorG+TotColorB-(TotColorRhu+TotColorGhu+TotColorBhu)) + chr(9) + repr(TotColorR+TotColorG+TotColorB-(TotColorRhl+TotColorGhl+TotColorBhl)) + ")  \n")
        else:
          out_file.write("Left, Center, Right " + repr(idx) + "=" + chr(9) + \
          repr(TotColorRvl+TotColorGvl+TotColorBvl) + "," + chr(9) + \
          repr(TotColorR+TotColorG+TotColorB) +  "," + chr(9) + \
          repr(TotColorRvr+TotColorGvr+TotColorBvr)+  \
          "("+repr(TotColorR+TotColorG+TotColorB-(TotColorRvl+TotColorGvl+TotColorBvl)) + chr(9) + repr(TotColorR+TotColorG+TotColorB-(TotColorRvr+TotColorGvr+TotColorBvr)) + ")  \n")
        
        fg.set(80, 0, over._bitmapapi()) # Draw overdrawing to allow user checking.
    out_file.write(repr(segm[0]) + repr(segm[1]) + repr(segm[2]) + repr(segm[3]) + repr(segm[4]) + repr(segm[5])  + repr(segm[6])+ "\n")
    out_file.write("threshold="+repr(threshold)+"\n")
    for f in range (0,9):
      if segm == Figures[f]:
        print "Rilevato un ",f
        out_file.write(repr(f) + "\n\n")
      else:
        pass #print "unknown figure"
        #out_file.write(repr(f+1) + "nothing)\n")
    #print "result=",segm

       
            
def Main():
  global offset, HWidth, VWidth, HHeight, VHeight, num,PixThreshold, img, switch
  running=1
  switch = 1  
  x=8
  y=10  
  XINC = 1
  XINC2 = 2
  YINC = 1
  YINC2 = 2
  YINC3 =4
  YINC4 = 4
  OFFSETINC = 10
  THRESHINC = 100
# create a loop to get stuff handled that needs to be done again and again
  while running:
      if switch == 2:
          Adjust()
      print switch
      if switch == 1:
          Reader()
      e32.ao_yield()
          

def quit():
    global running
    running=0
    out_file.close()
    appuifw.app.set_exit()

# define the redraw function (redraws the screen)
def handle_redraw(rect):
    pass
    #canvas.blit(img)


InitVars()


app.exit_key_handler = quit
capturer=keycapture.KeyCapturer(cb_capture)
capturer.forwarding=0
capturer.keys=(
               keycapture.EKey0,
               keycapture.EKey1,
               keycapture.EKey2,
               keycapture.EKey3,
               keycapture.EKey4,
               keycapture.EKey5,
               keycapture.EKey6,
               keycapture.EKey7,
               keycapture.EKey8,
               keycapture.EKey9,
               keycapture.EKeyYes,
               keycapture.EKeyNo,
               keycapture.EKeyEdit,
               keycapture.EKeyStar,
               #keycapture.EKeyUpArrow,
               #keycapture.EKeyDownArrow,
               keycapture.EKeyHash,
               keycapture.EKeyStar
               )
capturer.start()

out_file = open("e:\\LCD-debug.log","w")
Main()

script_lock = e32.Ao_lock()
script_lock.wait()


#appuifw.app.screen='normal'
# create an empty image
#img=Image.new((176,208))

# define the canvas including key scanning fucntion as callback and also the redraw handler as callback
#canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
# set the application body to canvas
#appuifw.app.body=canvas

#app.exit_key_handler=quit

# take a photo in of the size 160x120 pixels
#screen_picture = camera.take_photo(size = (160,120))






        


 


