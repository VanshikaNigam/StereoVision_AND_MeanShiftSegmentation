import numpy as np
import cv2
import sys


view1 = cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view1.png',0);
view5 = cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view5.png',0);
disp1=cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/disp1.png',0);
disp5=cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/disp5.png',0);

view1_with_border = cv2.copyMakeBorder(view1, 1, 1, 1, 1,cv2.BORDER_CONSTANT,value=0)
view5_with_border = cv2.copyMakeBorder(view5, 1, 1, 1, 1,cv2.BORDER_CONSTANT,value=0)
disp1_border=cv2.copyMakeBorder(disp1, 1, 1, 1, 1,cv2.BORDER_CONSTANT,value=0)
disp5_border=cv2.copyMakeBorder(disp5, 1, 1, 1, 1,cv2.BORDER_CONSTANT,value=0)

x,y=view1_with_border.shape
v,w=view5_with_border.shape

#https://stackoverflow.com/questions/36692484/python-extracting-a-smaller-matrix-from-a-larger-one
#def submatrix( matrix, startRow, startCol, size):
#return x[startRow:startRow+size,startCol:startCol+size]

disparity_map1=np.zeros((x,y))
disparity_map5=np.zeros((v,w))

#For 3x3 block left image 

for i in range(1,x-1):
    for j in range(1,y-1):
        view1_block=view1_with_border[i-1:i+2,j-1:j+2]
        #print view1_block
#https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
                
        min_ssd_l=sys.maxint
        min_ssd_index_l=-1
        
        for k in range(j-75,j):
            if(k<=1):
                k=1
            view5_block=view5_with_border[i-1:i+2,k-1:k+2]
            view_diff=np.square(view1_block-view5_block) #left image
        
            ssd_left=np.sum(view_diff)
            
            if (ssd_left <min_ssd_l):
                min_ssd_l=ssd_left
                min_ssd_index_l=k
            
        disparity_map1[i][j] = j-min_ssd_index_l;
       
#print disparity_map1
max_value=np.amax(disparity_map1)
display=disparity_map1/max_value
cv2.imshow("DMAP1_3x3_75",display)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/Block3X3_75_Left.png',disparity_map1)


#https://stackoverflow.com/questions/39064684/mean-squared-error-in-python

mse_left = np.mean((disp1_border-disparity_map1)**2)
print "MSE with respect to Left Image when the block is 3X3" , mse_left


#For 3x3 block right image 

for i in range(1,x-1):
    for j in range(1,y-1):
        
        view_block5=view5_with_border[i-1:i+2,j-1:j+2]
    
        min_ssd_r=sys.maxint
        min_ssd_index_r=-1
        
        for k in range(j+75,j,-1):
            if (k >= y-1):
                k=y-2
            
            view_block1=view1_with_border[i-1:i+2,k-1:k+2]
            view_differ=np.square(view_block5-view_block1) #right image
            ssd_right=np.sum(view_differ)
            
            if(ssd_right<min_ssd_r):
                min_ssd_r=ssd_right
                min_ssd_index_r=k
       
        disparity_map5[i][j]=min_ssd_index_r-j
        
max_value5=np.amax(disparity_map5)
display5=disparity_map5/max_value5

cv2.imshow("DMAP5_3x3_75",display5)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/Block3X3_75_Right.png',disparity_map5)

#https://stackoverflow.com/questions/39064684/mean-squared-error-in-python

mse_right=np.mean((disp5_border-disparity_map5)**2)
print "MSE with respect to Right Image when the block is 3X3" , mse_right

 
#Consistency Checking


consistency_left=np.zeros((x,y))
consistency_right=np.zeros((v,w))

#LEFT

for i in range (0,x):
    for j in range (0, y):
        pixel_value_l=disparity_map1[i,j]
        if y>j-pixel_value_l>0:
            pixel_value_r=disparity_map5[i,j-pixel_value_l]
        else:
            pixel_value_r=disparity_map5[i,j]
            
        if(pixel_value_l==pixel_value_r):
            consistency_left[i,j]=pixel_value_l
        else:
            consistency_left[i,j]=0

cv2.imshow("consistency_3x3_75L",consistency_left)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/consistency3X3_75_Left.png',consistency_left)


Sum_left=0
for i in range (0,x):
    for j in range(0,y):
        if(consistency_left[i,j]!=0):
            temp=(disp1_border[i,j]-consistency_left[i,j])**2
            Sum_left=Sum_left+temp


mse_c_left=Sum_left/(x*y)
print "MSE with respect to Leftt Image when the block is 3X3 after Consistency check" , mse_c_left

#mse_c_left=np.mean((consistency_left-disp1_border)**2)

#RIGHT

for i in range (0,x):
    for j in range (0, y):
        pixel_value_r=disparity_map5[i,j]
        if j+pixel_value_r<y:
            
            pixel_value_l=disparity_map1[i,j+pixel_value_r]
        else:
            pixel_value_l=disparity_map1[i,j]
                
        if(pixel_value_r==pixel_value_l):
            consistency_right[i,j]=pixel_value_r
        else:
            consistency_right[i,j]=0

cv2.imshow("consistency_3X3_75R",consistency_right)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/consistency3X3_75_Right.png',consistency_right)

Sum_right=0
for i in range (0,x):
    for j in range(0,y):
        if(consistency_right[i,j]!=0):
            temp=(disp5_border[i,j]-consistency_right[i,j])**2
            Sum_right=Sum_right+temp


mse_c_right=Sum_right/(x*y)
print "MSE with respect to Right Image when the block is 3X3 after Consistency check" , mse_c_right




            
        
        
    


