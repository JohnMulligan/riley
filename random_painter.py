import sys
import numpy
import random
from numpy.random import choice
import cv2
import time
import math
import messengers

M = int(sys.argv[1])
N = int(sys.argv[2])
iterations = int(sys.argv[3])

#color dict format:
#id:[(r,g,b),probability weight]
color_dict={
1:[(170,163,195),.2],
2:[(139,193,137),.2],
3:[(218,181,171),.2],
4:[(255,255,255),.4]
}


#canvas parameters
#going to hard code in a few values but really the whole layout should be explored as a 6-dimensional parameter space, with its own internal constraints

max_connectedness=2

#circle radius
r=25
#r2 is distance between circle centers
r2=65
#l is xy distance on grid between circle centers
l=r2/math.sqrt(2)


def draw_matrix(matrix,fname):
	M,N=matrix.shape
	#derive the canvas size from our item layout
	#drawing a diagonal matrix, the circles have overlaps
	##I like that -- it shows the white circles as subtractions
	W=int(l*(N-1))+2*r
	H=int(l*(M-1))+2*r
	img=numpy.full((H,W,3),(255,255,255),numpy.uint8)
	for m in range(M):
		for n in range(N):
			v=matrix[m][n]
			if v!=0:
				x=int(n*l+r)
				y=int(m*l+r)
				color=color_dict[v][0]
				img=cv2.circle(img,(x,y),r,color,-1)
	cv2.imwrite(fname,img)				
	

	
#illustrate the layout in stdout
messengers.make_checkerboard(M,N)

#make rect matrix
rect_matrix = messengers.make_rectangular_matrix(M,N)
#get transformations
RT,DT=messengers.transposition_indices(rect_matrix)
O=P = len(DT[0])

for iteration in range(iterations):
	rect_color_matrix = numpy.zeros((M,N))
	
	#pick colors for nodes
	matrix_colors = {}
	
	color_probabilities = [color_dict[k][1] for k in color_dict]
	color_keys = list(color_dict.keys())
	
	for m in range(M):
		for n in range(N):
			id=rect_matrix[m][n]
			if id != 0:
				color_key = choice(color_keys,p=color_probabilities)
				matrix_colors[id] = color_key
				rect_color_matrix[m][n]=color_key
	
	#now assign to diagonal matrix
	
	diag_color_matrix = messengers.transform(rect_color_matrix,RT,M,N,O,P)
	
	draw_matrix(rect_color_matrix,'%d_rect.png' %iteration)
	draw_matrix(diag_color_matrix,'%d_diag.png' %iteration)