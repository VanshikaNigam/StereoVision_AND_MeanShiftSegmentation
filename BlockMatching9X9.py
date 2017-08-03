import numpy as np
import cv2
import sys

view1 = cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view1.png',0);
view5 = cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view5.png',0);
disp1=cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/disp1.png',0);
disp5=cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/disp5.png',0);

view1_with_border = cv2.copyMakeBorder(view1, 4, 4, 4, 4,cv2.BORDER_CONSTANT,value=0)
view5_with_border = cv2.copyMakeBorder(view5, 4, 4, 4, 4,cv2.BORDER_CONSTANT,value=0)
disp1_border=cv2.copyMakeBorder(disp1, 4, 4, 4, 4,cv2.BORDER_CONSTANT,value=0)
disp5_border=cv2.copyMakeBorder(disp5, 4, 4, 4, 4,cv2.BORDER_CONSTANT,value=0)

#print view1_with_border
#print disp5_border.shape

x,y=view1_with_border.shape
v,w=view5_with_border.shape

#https://stackoverflow.com/questions/36692484/python-extracting-a-smaller-matrix-from-a-larger-one
#def submatrix( matrix, startRow, startCol, size):
#    return x[startRow:startRow+size,startCol:startCol+size]

disparity_map1=np.zeros((x,y))
disparity_map5=np.zeros((v,w))

#For 9x9 block left image 

for i in range(4,x-4):
    for j in range(4,y-4):
        view1_block=view1_with_border[i-4:i+5,j-4:j+5]
        
        min_ssd=sys.maxint
        min_ssd_index=-1
        
        for k in range(j-75,j):
            if(k<=5):
                k=5
            view5_block=view5_with_border[i-4:i+5,k-4:k+5]
        
            view_diff=np.square(view1_block-view5_block) #left image
            ssd=np.sum(view_diff)
            
            #print ssd
            if (ssd <min_ssd):
                min_ssd=ssd
                min_ssd_index=k
            
        disparity_map1[i][j] = j-min_ssd_index;
       
#print disparity_map1
max_value=np.amax(disparity_map1)
#print max_value
display=disparity_map1/max_value
#print display
cv2.imshow("DMAP1_9x9_75",display)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/Block9X9_75_Left.png',disparity_map1)


#https://stackoverflow.com/questions/39064684/mean-squared-error-in-python

mse_left = np.mean((disp1_border-disparity_map1)**2)
print "MSE with respect to Left Image when the block is 9X9:",mse_left

#For 3x3 block right image 

for i in range(4,x-4):
    for j in range(4,y-4):
        
        view_block5=view5_with_border[i-4:i+5,j-4:j+5]
        
        min_ssd_r=sys.maxint
        min_ssd_index_r=-1
        
        for k in range(j+75,j,-1):
            if (k >= y-5):
                k=y-6
    
            view_block1=view1_with_border[i-4:i+5,k-4:k+5]
           
            view_differ=np.square(view_block5-view_block1) #right image
            ssd_right=np.sum(view_differ)
           
            
            if(ssd_right<min_ssd_r):
                min_ssd_r=ssd_right
                min_ssd_index_r=k
       
        
        disparity_map5[i][j]=min_ssd_index_r-j

max_value5=np.amax(disparity_map5)
display5=disparity_map5/max_value5

cv2.imshow("DMAP5_9x9_75",display5)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/Block9X9_75_Right.png',disparity_map5)


#https://stackoverflow.com/questions/39064684/mean-squared-error-in-python

mse_right=np.mean((disp5_border-disparity_map5)**2)
print "MSE with respect to Right Image when the block is 9X9:",mse_right

#consistency

consistency_left=np.zeros((x,y))
consistency_right=np.zeros((v,w))

for i in range (4,x-4):
    for j in range (4, y-4):
        pixel_value_l=disparity_map1[i,j]
        if j-pixel_value_l>0:
            pixel_value_r=disparity_map5[i,j-pixel_value_l]
        else:
            pixel_value_r=disparity_map5[i,j]
            
        if(pixel_value_l==pixel_value_r):
            consistency_left[i,j]=pixel_value_l
        else:
            consistency_left[i,j]=0

cv2.imshow("consistency_9x9_75L",consistency_left/consistency_left.max())
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/consistency9X9_75_Left.png',consistency_left)

Sum_left=0
for i in range (0,x):
    for j in range(0,y):
        if(consistency_left[i,j]!=0):
            temp=(disp1_border[i,j]-consistency_left[i,j])**2
            Sum_left=Sum_left+temp


mse_c_left=Sum_left/(x*y)
print "MSE with respect to Leftt Image when the block is 9X9 after Consistency check" , mse_c_left


for i in range (4,x-4):
    for j in range (4, y-4):
        pixel_value_r=disparity_map5[i,j]
        if j+pixel_value_r<y-4:
            
            pixel_value_l=disparity_map1[i,j+pixel_value_r]
        else:
            pixel_value_l=disparity_map1[i,j]
                
        if(pixel_value_r==pixel_value_l):
            consistency_right[i,j]=pixel_value_r
        else:
            consistency_right[i,j]=0

cv2.imshow("consistency_9X9_75R",consistency_right/consistency_right.max())
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/consistency9X9_75_Right.png',consistency_right)

Sum_right=0
for i in range (0,x):
    for j in range(0,y):
        if(consistency_right[i,j]!=0):
            temp=(disp5_border[i,j]-consistency_right[i,j])**2
            Sum_right=Sum_right+temp


mse_c_right=Sum_right/(x*y)
print "MSE with respect to Right Image when the block is 9X9 after Consistency check" , mse_c_right




