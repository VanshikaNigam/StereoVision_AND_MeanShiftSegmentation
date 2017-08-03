import numpy as np
import cv2


image_1 = cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view1.png')
image_2= cv2.imread('/Users/vanshika/Desktop/CVIP/PA2Data/view5.png')
left_img= cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
right_img= cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/view1_gray.png',left_img)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/view5_gray.png',right_img)

x,y=left_img.shape
v,w=right_img.shape
#print "left image dimension",x,y
#print "right image dimension",v,w

DisparityMatrix_left=np.zeros(left_img.shape, np.uint8)
DisparityMatrix_right=np.zeros(right_img.shape, np.uint8)
#DisparityMatrix_left.astype(int)
#DisparityMatrix_right.astype(int)

#Disparity Computation for Left Image

OcclusionCost = 20 #(You can adjust this, depending on how much threshold you want to give for noise)

#For Dynamic Programming you have build a cost matrix. Its dimension will be numcols x numcols
for all_rows in range (0,x):
    #print all_rows
    CostMatrix=np.zeros((y,y))
    
    DirectionMatrix = np.zeros((y,y))  #(This is important in Dynamic Programming. You need to know which direction you need traverse)
    
    #We first populate the first row and column values of Cost Matrix
    
    for i in range(0,y):
        CostMatrix[i,0] = i*OcclusionCost
        CostMatrix[0,i] = i*OcclusionCost
        
        #print np.abs((left_img[all_rows,0]-right_img[all_rows,0]))
    
    for i in range(0,y):
        for j in range (0,y):
            min1=CostMatrix[i-1,j-1]+np.abs((int(left_img[all_rows,i])-int(right_img[all_rows,j])))
            min2=CostMatrix[i-1,j]+OcclusionCost
            min3=CostMatrix[i,j-1]+OcclusionCost
            cmin=np.min((min1,min2,min3))
            
            CostMatrix[i,j]=cmin
            if min1==cmin:
                DirectionMatrix[i,j]=1
            if min2==cmin:
                DirectionMatrix[i,j]=2
            if min3==cmin:
                DirectionMatrix[i,j]=3
                   
        #print DirectionMatrix
        # Now, its time to populate the whole Cost Matrix and DirectionMatrix
        
        # Use the pseudocode from "A Maximum likelihood Stereo Algorithm" paper given as reference
        p=y-1
        q=y-1
        
        #print q
        #print p

    while ((p!=0) and (q!=0)):
        #print "Values for direction matrix"
        #print(DirectionMatrix[p,q])
        if DirectionMatrix[p,q]==1:
            #print("inside 1")
            DisparityMatrix_left[all_rows,p]=np.abs(p-q)
            DisparityMatrix_right[all_rows,q]=np.abs(p-q)
            p=p-1
            q=q-1
            
        elif DirectionMatrix[p,q]==2:
            #print("inside 2")
            p=p-1
            # DisparityMatrix_left[all_rows,p]=np.abs(p-q)
            
           
        elif DirectionMatrix[p,q]==3:
            #print("inside 3")
            q=q-1
            # DisparityMatrix_right[all_rows,q]=np.abs(p-q)
           
            
    
    #print "Left"
    #print DisparityMatrix_left
    #print "Right"
    #print DisparityMatrix_right
    
print DisparityMatrix_left
print "###################"
print DisparityMatrix_right  

  
cv2.imshow("left image",DisparityMatrix_left)
cv2.imshow("right image",DisparityMatrix_right)  
             
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/img_L_DP.png',DisparityMatrix_left)
cv2.imwrite('/Users/vanshika/Desktop/CVIP/PA2Data/img_R_DP.png',DisparityMatrix_right)
print "done"


        
    
    

