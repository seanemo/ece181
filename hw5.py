from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from skimage import io 
import cv2 as cv


img1 = io.imread('left.jpg')#left checkerboard image
img2 = io.imread('right.jpg')#right checkerboard image

def FundamentalMatrix():#finds Fundamental matrix between two images
    

    plt.imshow(img1)#select points from left image
    points_left = plt.ginput(8, 0)

    plt.imshow(img2)#select points from right image
    points_right = plt.ginput(8, 0)

    pts1 = np.asarray(points_left)#sets both lists into arrays
    pts2 = np.asarray(points_right)

    F = cv.findFundamentalMat(pts1, pts2, cv.FM_8POINT)#calculates fundamental matrix of the two images
    
    return F

#F = FundamentalMatrix()
#print(F)

def addPoint(x,y,left_img):#function indicates specified point on left image
    img = cv.circle(left_img, (x,y), 5, (0,0,255),-1)
    return img

def drawEpipolarLine(x,y,right_img):#draws corresponding epipolar line on the right image 

    #Fundamental matrix of the two images
    F = np.array([[ 9.80685473e-06,  3.46773351e-05, -1.01493607e-02],
       [-3.15451267e-05,  1.75641034e-05, -3.32954052e-03],
       [ 6.78487085e-03, -4.79648337e-03,  1.00000000e+00]])

    point = np.array([[x],[y],[1.0]])#converts specified cartesian point into a homogeneous point
    line = np.matmul(F,point)#calculates epipole line in homogeneous coordinates

    a, b, c = line[0], line[1], line[2] #labels each element of the line
    x0 = 0 
    y0 = int(-c/b) #gets the y-coordinate of a point on the line when x = 0
    x1 = len(right_img[0])
    y1 = int(-(a*x1+c)/b) # gets the y-coordinate of a point on the epipolar line when x is the length of the image
    line_img = cv.line(right_img, (x0,y0),(x1,y1), (0,0,255), 1)#draws the line on the right image

    return line_img

#change x and y coordinates in the following lines to change the specified point
img2 = drawEpipolarLine(183, 100, img2) #draws the epipolar line
img1 = addPoint(183, 100, img1) # indicates the point on the left image

img_h = cv.hconcat([img1,img2]) #concats the two images


plt.imshow(img_h)#output
plt.show()

