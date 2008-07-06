# Nokia Data Logger - PC version
# This program analyses images obtained by NDL started on the phone,
# attempting to recognize LCD numbers.

# Program requires needed images to be present into FOLDERNAME folder.
# Results are stored into LOGFILENAME in same folder.
import Image, ImageDraw

FOLDERNAME = u'C:\\temp\\lcd\\'
LOGFILENAME = u'LCD-debug.log'

TopLeftX = [ 79, 000, 000, 000, 000, 000, 000] #46, 79, 118
TopLeftY = [ 103, 000, 000, 160, 000, 000, 000]
HWidth = 20
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
  global TopLeftX, TopLeftY , HHeight, HWidth, VHehight, VWidth , offset, num, threshold, figures, segm, FOLDERNAME,average
  
  KBLACK = 10
  KWHITE = 16777215
  TopLeftY[6] = (TopLeftY[3] + TopLeftY[0])/2
  TopLeftY[1] = TopLeftY[0]+ HHeight
  TopLeftY[2] = TopLeftY[6]+ HHeight
  TopLeftY[4] = TopLeftY[2]
  TopLeftY[5] = TopLeftY[1]
  TopLeftX[1]=TopLeftX[0]+HWidth
  TopLeftX[2]=TopLeftX[1]-2
  TopLeftX[3]=TopLeftX[0]
  TopLeftX[4] = TopLeftX[0] - VWidth -2 
  TopLeftX[5] = TopLeftX[0] - VWidth + 1
  TopLeftX[6] = TopLeftX[0] 
  
  filecount = 1
  filenum = Lead0(filecount)
  filename=(FOLDERNAME + 'LCD' + filenum + '.jpg')
  
  filename = FOLDERNAME +  u'LCD20080706_162757.jpg'
  img = Image.open(filename)
  img=img.convert('L')
  img=img.convert('RGB')
  out_file = open(FOLDERNAME + LOGFILENAME,'w')
  
  average = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
 
  for n in range(1): # Loop through various figures
    for idx in range(7): # Loop through segments.
        #print idx
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
        average[idx][1]= (TotColorR+TotColorG+TotColorB) / ((Xend-Xstart)*(Yend-Ystart))
        print "idx=",idx, ", center=",average[idx][1]
            
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
                colore = KWHITE-1000
              else:
                colore = KBLACK+100
              img.putpixel((x,y),colore)
          average[idx][2]= (TotColorRhl+TotColorGhl+TotColorBhl) / ((Xend-Xstart)*(Yend-Ystart))    
          for x in range(Xstart, Xend): # Horizontal segment upper neighbour
            for y in range(Ystart-HHeight, Yend-HHeight):
              tempR, tempG, tempB =  img.getpixel((x,y))#[0]
              TotColorRhu = TotColorRhu + tempR
              TotColorGhu = TotColorGhu + tempG
              TotColorBhu = TotColorBhu + tempB 
              if TotColorRhu+TotColorGhu+TotColorBhu > threshold:
                colore = KWHITE-1000
              else:
                colore = KBLACK+100
              img.putpixel((x,y),colore)
          average[idx][0]= (TotColorRhu+TotColorGhu+TotColorBhu) / ((Xend-Xstart)*(Yend-Ystart))   
        #    *** VERTICAL **
        else: 
          for x in range(Xstart+VWidth, Xend+VWidth): # Vertical segment right neighbour
            for y in range(Ystart, Yend):
              tempR, tempG, tempB =  img.getpixel((x,y))#[0]
              TotColorRvr = TotColorRvr + tempR
              TotColorGvr = TotColorGvr + tempG
              TotColorBvr = TotColorBvr + tempB 
              if TotColorRvr+TotColorGvr+TotColorBvr > threshold:
                colore = KWHITE-1000
              else:
                colore = KBLACK+100
              img.putpixel((x,y),colore)
          average[idx][2]= (TotColorRvr+TotColorGvr+TotColorBvr) / ((Xend-Xstart)*(Yend-Ystart))    
          for x in range(Xstart-VWidth, Xend-VWidth): # Vertical segment left neighbour
            for y in range(Ystart, Yend):
              tempR, tempG, tempB =  img.getpixel((x,y))#[0]
              TotColorRvl = TotColorRvl + tempR
              TotColorGvl = TotColorGvl + tempG
              TotColorBvl = TotColorBvl + tempB 
              if TotColorRvl+TotColorGvl+TotColorBvl > threshold:
                colore = KWHITE-1000
              else:
                colore = KBLACK+100
              img.putpixel((x,y),colore)
          average[idx][0]= (TotColorRvl+TotColorGvl+TotColorBvl) / ((Xend-Xstart)*(Yend-Ystart))
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
  
  d = ImageDraw.Draw(img)
  for co in range(0,7):
    print average[co], average[co][1]-average[co][0], average[co][1]-average[co][2]

  print TopLeftX[0],TopLeftY[0], HWidth, VWidth
  d.rectangle([TopLeftX[0],TopLeftY[0],TopLeftX[0]+HWidth,TopLeftY[0]+HHeight],fill=(average[0][1]/3,average[0][1]/3,average[0][1]/3))
  d.rectangle([TopLeftX[0],TopLeftY[0]-HHeight,TopLeftX[0]+HWidth,TopLeftY[0]+HHeight-HHeight],fill=(average[0][0]/3,average[0][0]/3,average[0][0]/3))
  d.rectangle([TopLeftX[0],TopLeftY[0]+HHeight,TopLeftX[0]+HWidth,TopLeftY[0]+HHeight+HHeight],fill=(average[0][2]/3,average[0][2]/3,average[0][2]/3))

  d.rectangle([TopLeftX[1],       TopLeftY[1],TopLeftX[1]+VWidth,       TopLeftY[1]+VHeight],fill=(average[1][1]/3,average[1][1]/3,average[1][1]/3))
  d.rectangle([TopLeftX[1]-VWidth,TopLeftY[1],TopLeftX[1]+VWidth-VWidth,TopLeftY[1]+VHeight],fill=(average[1][0]/3,average[1][0]/3,average[1][0]/3))
  d.rectangle([TopLeftX[1]+VWidth,TopLeftY[1],TopLeftX[1]+VWidth+VWidth,TopLeftY[1]+VHeight],fill=(average[1][2]/3,average[1][2]/3,average[1][2]/3))

  d.rectangle([TopLeftX[2],       TopLeftY[2],TopLeftX[2]+VWidth,       TopLeftY[2]+VHeight],fill=(average[2][1]/3,average[2][1]/3,average[2][1]/3))
  d.rectangle([TopLeftX[2]-VWidth,TopLeftY[2],TopLeftX[2]+VWidth-VWidth,TopLeftY[2]+VHeight],fill=(average[2][0]/3,average[2][0]/3,average[2][0]/3))
  d.rectangle([TopLeftX[2]+VWidth,TopLeftY[2],TopLeftX[2]+VWidth+VWidth,TopLeftY[2]+VHeight],fill=(average[2][2]/3,average[2][2]/3,average[2][2]/3))

  d.rectangle([TopLeftX[3],TopLeftY[3],        TopLeftX[3]+HWidth,TopLeftY[3]+HHeight],        fill=(average[3][1]/3,average[3][1]/3,average[3][1]/3))
  d.rectangle([TopLeftX[3],TopLeftY[3]-HHeight,TopLeftX[3]+HWidth,TopLeftY[3]+HHeight-HHeight],fill=(average[3][0]/3,average[3][0]/3,average[3][0]/3))
  d.rectangle([TopLeftX[3],TopLeftY[3]+HHeight,TopLeftX[3]+HWidth,TopLeftY[3]+HHeight+HHeight],fill=(average[3][2]/3,average[3][2]/3,average[3][2]/3))

  d.rectangle([TopLeftX[4],       TopLeftY[4],TopLeftX[4]+VWidth,       TopLeftY[4]+VHeight],fill=(average[4][1]/3,average[4][1]/3,average[4][1]/3))
  d.rectangle([TopLeftX[4]-VWidth,TopLeftY[4],TopLeftX[4]+VWidth-VWidth,TopLeftY[4]+VHeight],fill=(average[4][0]/3,average[4][0]/3,average[4][0]/3))
  d.rectangle([TopLeftX[4]+VWidth,TopLeftY[4],TopLeftX[4]+VWidth+VWidth,TopLeftY[4]+VHeight],fill=(average[4][2]/3,average[4][2]/3,average[4][2]/3))

  d.rectangle([TopLeftX[5],       TopLeftY[5],TopLeftX[5]+VWidth,       TopLeftY[5]+VHeight],fill=(average[5][1]/3,average[5][1]/3,average[5][1]/3))
  d.rectangle([TopLeftX[5]-VWidth,TopLeftY[5],TopLeftX[5]+VWidth-VWidth,TopLeftY[5]+VHeight],fill=(average[5][0]/3,average[5][0]/3,average[5][0]/3))
  d.rectangle([TopLeftX[5]+VWidth,TopLeftY[5],TopLeftX[5]+VWidth+VWidth,TopLeftY[5]+VHeight],fill=(average[5][2]/3,average[5][2]/3,average[5][2]/3))

  d.rectangle([TopLeftX[6],TopLeftY[6],        TopLeftX[6]+HWidth,TopLeftY[6]+HHeight],        fill=(average[6][1]/3,average[6][1]/3,average[6][1]/3))
  d.rectangle([TopLeftX[6],TopLeftY[6]-HHeight,TopLeftX[6]+HWidth,TopLeftY[6]+HHeight-HHeight],fill=(average[6][0]/3,average[6][0]/3,average[6][0]/3))
  d.rectangle([TopLeftX[6],TopLeftY[6]+HHeight,TopLeftX[6]+HWidth,TopLeftY[6]+HHeight+HHeight],fill=(average[6][2]/3,average[6][2]/3,average[6][2]/3))

  img.show()
    

Start()        




