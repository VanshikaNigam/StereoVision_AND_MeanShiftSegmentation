import numpy as np
import cv2

view1 = cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view1.png');
view5 = cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view5.png');
disp1=cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/disp1.png',0);
disp5=cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/disp5.png',0);

x,y,z= view1.shape
#print view5.shape

view_synthesis=np.zeros((x,y,z),np.uint8)
#filled = np.zeros((x,y), np.uint8)
count = 0

for i in range (0,x):
    for j in range (0,y):
        distance_l=disp1[i,j]
        mid_index=distance_l/2
        #if (j-mid_index>=0)and(j-mid_index<=y):
        if j-mid_index < 0:
            # print 'empty'
            # count += 1
            continue
        view_synthesis[i,j-mid_index]=view1[i,j]
        #filled[i,j-mid_index] = 1
        
#print view_synthesis
#print count
cv2.imshow("S1",view_synthesis)  
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/1stPic.png',view_synthesis) 

"""
print "left"
for i in range (0,x):
    for j in range (0, y):
        if view_synthesis[i,j].all()==0:
            print view_synthesis[i,j]
            count=count+1
            print "count value",count
            print "index", i,j
    break;                           

"""
for n in range (0,x):
    for m in range (0,y):
        distance_r=disp5[n,m]
        mid=distance_r/2
        #print distance_r
        if m+mid>=y:
            continue
        #if (j+mid>=0)and(j+mid<=y):
    
        if view_synthesis[n,m+mid].all() == 0:
                # print 'filling',view_synthesis[n][m+mid]
                #count -= 1
                view_synthesis[n,m+mid]=view5[n,m]
                
#print view_synthesis
#print count
cv2.imshow("S2",view_synthesis) 
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/FinalPic.png',view_synthesis)                              
               
"""
for i in range (0,x):
    for j in range (0, y):
        if view_synthesis[i,j].all()==0:
            print view_synthesis[i,j]
    break;
"""        
        