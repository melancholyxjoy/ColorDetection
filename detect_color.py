# import the necessary packages
import numpy as np
import argparse
import cv2
import socket

from cv2 import *

UDP_IP = "10.51.15.2"
UDP_PORT = 8005

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

count = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# load the image
cam = VideoCapture(0)
s, image = cam.read()

if s:
	#namedWindow("cam-test",1)
	#imshow("cam-test",image)
	#waitKey(0)
	#destroyWindow("cam-test")
	imread(args["image"])

# define the list of boundaries
boundaries = [
	([192, 67, 67], [224, 30, 30]),
	([67, 67, 192], [30, 30, 224]),
	([103, 86, 65], [145, 133, 128])
]

# loop over the boundaries
for (lower, upper) in boundaries:

	count += 1	

	# Convert from RGB to HSV
	hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

	# Create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
 	
	# Find the colors within the specified boundaries and apply
	# The mask
	mask = cv2.inRange(hsv, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)
	
	#Count number of pixels
	numnBlk = cv2.countNonZero(mask)
	print("The number of non black pixels is: " + str(numnBlk))

	if count == 1:
		red = numnBlk
		print(red)
	elif count == 2:
		blue = numnBlk
		print(blue)
	elif count == 3:
		grey = numnBlk
		print(grey)

	# show the images
	cv2.imshow("images", np.hstack([output]))
	cv2.waitKey(0)

if red > blue & grey:
	MESSAGE = "Red"
elif blue > red & grey:
	MESSAGE = "Blue"
elif grey > red & blue:
	MESSAGE = "Neutral"

print(MESSAGE)
#socket.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

