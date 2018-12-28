import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import binascii
import os
import argparse
import socket
import colorsys
import cv2

from cv2 import *
from PIL import Image

NUM_CLUSTERS = 5

UDP_IP = "10.51.15.2"
UDP_PORT = "8005"

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

count = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

print("Reading")

cam = VideoCapture(0)
s, image = cam.read()

if s:
	namedWindow("test", 1)
	imshow("test",image)
	waitKey(0)
	destroyWindow("test")
	imwrite("filename.jpg",image)
	imread(args["image"])

im = Image.open("filename.jpg")
im = im.resize((150,150))
ar = np.asarray(im)
shape = ar.shape
ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

print("Finding")

codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

print("Cluster Centers:\n",codes)

vecs, dist = scipy.cluster.vq.vq(ar, codes)
counts, bins = scipy.histogram(vecs, len(codes))

index_max = scipy.argmax(counts)
peak = codes[index_max]
color = binascii.b2a_hex(peak)
print("most frequent is %s (#%s)" % (peak,color))

COLO = colorsys.rgb_to_hsv(peak[0],peak[1],peak[2])

colorrange = [
	([COLO[0],COLO[1],COLO[2]], [COLO[0] + 10,COLO[1] + 10,COLO[2] + 10])
]

for (lower, upper) in colorrange:
	count += 1

	# Create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
 	
	# Find the colors within the specified boundaries and apply
	# The mask
	mask = cv2.inRange(image, lower, upper)
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

if red:
	MESSAGE = "Red"

print(MESSAGE)
#socket.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
try:
	os.remove("filename.jpg")
except: pass
