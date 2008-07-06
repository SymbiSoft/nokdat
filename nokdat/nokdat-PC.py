# Nokia Data Logger - PC version
# This program analyses images obtained by NDL started on the phone,
# attempting to recognize LCD numbers.

# Program requires needed images to be present into FOLDERNAME folder.
# Results are stored into LOGFILENAME in same folder.
import Image

FOLDERNAME = u'C:\\temp\\lcd\\'
LOGFILENAME = u'LCD-debug.log'

TopLeftX = [ 81, 000, 000, 000, 000, 000, 000]
TopLeftY = [ 103, 000, 000, 160, 000, 000, 000]
HWidth = 26
HHeight = 5
VWidth = HHeight
VHeight = HWidth

offset = 70
num=[0,offset,2*offset,3*offset,4*offset,5*offset] 

threshold = 12000

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
         
segm=[2,2,2,2,2,2,2]

def Lead0(n):
  temp = '';
  if n < 10:
    temp = temp + '0'      
  if n < 100:
    temp = temp + '0'      
  if n < 1000:
    temp = temp + '0'      
  if n < 10000:
    temp = temp + '0'  
  return temp   + `n` 
  

def Start():
  global TopLeftX, TopLeftY , HHeight, HWidth, VHehight, VWidth , offset, num, threshold, figures, segm, FOLDERNAME
  
  KBLACK = 10
  KWHITE = 65000
  TopLeftY[6] = (TopLeftY[3] + TopLeftY[0])/2
  TopLeftY[1] = TopLeftY[0]+ HHeight
  TopLeftY[2] = TopLeftY[6]+ HHeight
  TopLeftY[4] = TopLeftY[2]
  TopLeftY[5] = TopLeftY[1]
  TopLeftX[1]=TopLeftX[0]+HWidth
  TopLeftX[2]=TopLeftX[1]-1
  TopLeftX[3]=TopLeftX[0]
  TopLeftX[4] = TopLeftX[0] - VWidth-1
  TopLeftX[5] = TopLeftX[0] - VWidth
  TopLeftX[6] = TopLeftX[0] 
  
  filecount = 1
  filenum = Lead0(filecount)
  filename=(FOLDERNAME + 'LCD' + filenum + '.jpg')
  
  filename = FOLDERNAME +  u'LCD20080706_162757.jpg'
  img = Image.open(filename)
  
  out_file = open(FOLDERNAME + LOGFILENAME,'w')
 
  for n in range(1): # Loop through various figures
    for idx in range(7): # Loop through segments.
        print idx
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
        # the segment is on (= black = under threshold) or off (= white = over threshold).
        
        if (idx == 0) or (idx == 6) or (idx == 3): # ******* Horizontal segments
          Xstart = num[n]+TopLeftX[idx]
          Xend = num[n]+TopLeftX[idx]+HWidth
          Ystart = TopLeftY[idx]
          Yend = TopLeftY[idx]+HHeight   
        else:                                      # ******* Vertical segments
          Xstart = num[n]+TopLeftX[idx]
          Xend = num[n]+TopLeftX[idx]+VWidth
          Ystart = TopLeftY[idx]
          Yend = TopLeftY[idx]+VHeight    
                   
        for x in range(Xstart, Xend): # sum up color of each pixel of the segment:
          for y in range(Ystart, Yend):
            tempR, tempG, tempB =  img.getpixel((x,y))#[0]
            TotColorR = TotColorR + tempR
            TotColorG = TotColorG + tempG
            TotColorB = TotColorB + tempB 
            if TotColorR+TotColorG+TotColorB > threshold:
              colore = KWHITE
            else:
              colore = KBLACK
            img.putpixel((x,y),colore)
            
        #  ******** Neighbours *******   
        
        #  *** HORIZONTAL **         
        if (idx == 0) or (idx == 6) or (idx == 3): # Horizontal segments neighbours
          for x in range(Xstart, Xend): # Horizontal segment lower neighbour
            for y in range(Ystart+HHeight, Yend+HHeight):
              tempR, tempG, tempB =  img.getpixel((x,y))#[0]
              TotColorRhl = TotColorRhl + tempR
              TotColorGhl = TotColorGhl + tempG
              TotColorBhl = TotColorBhl + tempB 
              if TotColorRhl+TotColorGhl+TotColorBhl > threshold:
                colore = KWHITE
              else:
                colore = KBLACK
              img.putpixel((x,y),colore)
          for x in range(Xstart, Xend): # Horizontal segment upper neighbour
            for y in range(Ystart-HHeight, Yend-HHeight):
              tempR, tempG, tempB =  img.getpixel((x,y))#[0]
              TotColorRhu = TotColorRhu + tempR
              TotColorGhu = TotColorGhu + tempG
              TotColorBhu = TotColorBhu + tempB 
              if TotColorRhu+TotColorGhu+TotColorBhu > threshold:
                colore = KWHITE
              else:
                colore = KBLACK
              img.putpixel((x,y),colore)
              
        #    *** VERTICAL **
        else: 
          for x in range(Xstart+VWidth, Xend+VWidth): # Vertical segment right neighbour
            for y in range(Ystart, Yend):
              tempR, tempG, tempB =  img.getpixel((x,y))#[0]
              TotColorRvr = TotColorRvr + tempR
              TotColorGvr = TotColorGvr + tempG
              TotColorBvr = TotColorBvr + tempB 
              if TotColorRvr+TotColorGvr+TotColorBvr > threshold:
                colore = KWHITE
              else:
                colore = KBLACK
              img.putpixel((x,y),colore)
          for x in range(Xstart-VWidth, Xend-VWidth): # Vertical segment left neighbour
            for y in range(Ystart, Yend):
              tempR, tempG, tempB =  img.getpixel((x,y))#[0]
              TotColorRvl = TotColorRvl + tempR
              TotColorGvl = TotColorGvl + tempG
              TotColorBvl = TotColorBvl + tempB 
              if TotColorRvl+TotColorGvl+TotColorBvl > threshold:
                colore = KWHITE
              else:
                colore = KBLACK
              img.putpixel((x,y),colore)
        if TotColorR+TotColorG+TotColorB > threshold: # If white, then off.
        #   print "white" 
  #         if (idx == 0) or (idx == 6) or (idx == 3): # Horizontal segments
  #          over.rectangle((Xstart,Ystart,Xstart+HWidth,Ystart+HHeight),0x000000,0xaaaaaa) 
  #         else:
  #          over.rectangle((Xstart,Ystart,Xstart+VWidth,Ystart+VHeight),0x000000,0xaaaaaa) 
           segm[idx]=0
        else:
          # print "black"
   #        if (idx == 0) or (idx == 6) or (idx == 3): 
   #          over.rectangle((Xstart,Ystart,Xstart+HWidth,Ystart+HHeight),0x000000,0x333333) 
   #        else:
   #          over.rectangle((Xstart,Ystart,Xstart+VWidth,Ystart+VHeight),0x000000,0x333333)            
           segm[idx]=1
        if (idx == 0) or (idx == 6) or (idx == 3):           
          out_file.write("Up  "+ chr(9) +"Mid   "+ chr(9) +"Down  " + repr(idx) + "=" + chr(9) + \
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
  #img.save(u'c:\\temp\\lcd\\output.bmp',quality=100)
  img.show('True')

Start()        
