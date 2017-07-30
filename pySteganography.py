import cv2
import numpy as np
import argparse


def encodeThis(oB, oG, oR, data):
	#encoding algorithm ::
	red= oR & 248
	green= oG & 248
	blue= oB & 252
 	if data & 128 == 128:
		red = red | 4 
	if data & 64 == 64:
		red = red | 2
	if data & 32 == 32:
		red = red | 1 
	if data & 16 == 16:
		green = green | 4 
	if data & 8 == 8:
		green = green | 2
	if data & 4 == 4:
		green = green | 1 
	if data & 2 == 2:
		blue = blue | 2
	if data & 1 == 1:
		blue = blue | 1
	return blue, green, red

def decodeMessage(target):
	#driver function for decoding algorithm ::
	dataDecoded = ''
	for i in range(target.shape[0]):
		for j in range(target.shape[1]):
			#original pixel values::
			t1 = target[i, j, 0]
			t2 = target[i, j, 1]
			t3 = target[i, j, 2]
			charData = decodeThis(t1,t2,t3)
			dataDecoded += chr(charData)
	return dataDecoded

def decodeThis(t1, t2, t3):
	#decoding algorithm ::
	txt=0;
	redc = t3
	bluec = t1
	greenc = t2
	if redc & 4 == 4:
		txt = txt | 128
	if redc & 2 == 2:
		txt = txt | 64
	if redc & 1 == 1:
		txt = txt | 32
	if greenc & 4 == 4:
		txt = txt | 16
	if greenc & 2 == 2:
		txt = txt | 8
	if greenc & 1 == 1:
		txt = txt | 4
	if bluec & 2 == 2:
		txt = txt | 2
	if bluec & 1 == 1:
		txt = txt | 1
	return txt

parser = argparse.ArgumentParser()
parser.add_argument('-s',help = 'Enter path to the image into which the text has to be embedded.')
parser.add_argument('-f',help = 'Enter path to the text file to encode.')
parsed = parser.parse_args()
source = cv2.imread(parsed.s)
target = np.zeros((source.shape[0], source.shape[1], source.shape[2]), np.uint8)

#read the source image and the source text file::
with open(parsed.f, 'r') as file:
    data=file.read().replace('\n', '')

imageSize = len(np.ravel(source))

textSize = len(data)

if(textSize > imageSize):
	print("Text File too large to encode!")

#append fullstops to the text encoded to maintain consistency::

else:
	while textSize < imageSize:
		data += '.'
		textSize = len(data)
	k = 0
	for i in range(source.shape[0]):
		for j in range(source.shape[1]):
			#original pixel values::
			o1 = source[i, j, 0]
			o2 = source[i, j, 1]
			o3 = source[i, j, 2]

			t1, t2, t3 = encodeThis(o1, o2, o3, ord(data[k]))
			k += 1
			#image with the embedded message::
			target[i, j, 0] = t1
			target[i, j, 1] = t2
			target[i, j ,2] = t3

	cv2.imshow('source', source)
	cv2.imshow('target', target)
	cv2.imwrite('target.tif', target)

	k = cv2.waitKey(0)
	
	cv2.destroyAllWindows()

	if k & 0xFF == ord('d'):
		target = cv2.imread('target.tif')
		print decodeMessage(target)
