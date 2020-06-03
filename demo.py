import sys
import numpy
from numpy.random import choice
import math
import visualizers
import messengers

#This script demonstrates usage of
###messengers.py (which handles matrix generation and transformation) with
###visualizers.py (which can currently generate visualizations in 3 formats:
#####text printouts of matrices, opencv-generated png's, and .html files with fabric.js interactivity

#Currently, I've hard-coded in:
##The color palette and relative probability for each color
##The radius of and distance between each node

#It therefore only handles two inputs: the number of rows (M) and columns (M)
#in the Riley matrix you want it to generate

#INTAKE MATRIX DIMENSIONS

#default number of iterations to run is 1

M = int(sys.argv[1])
N = int(sys.argv[2])
iterations = int(sys.argv[3]) if len(sys.argv) >=4 else 1

#SET COLOR PALETTE

#color dict format:
#id:[(r,g,b),probability weight,name]
#use only sequential natural numbers, starting from 1.
#Breaking sequence or using 0 will mess up messengers.py
color_dict={
1:[(170,163,195),.2,'purple'],
2:[(139,193,137),.2,'green'],
3:[(218,181,171),.2,'salmon'],
4:[(255,255,255),.4,'white']
}


#SET CANVAS PARAMETERS 

##hard-coded in a few values
##but really the whole layout should be explored as a 6-dimensional parameter space, with its own internal constraints
##circle radius
r=25
#L values are the distances between circle centers
diag_L=65
rect_L=diag_L/math.sqrt(2)



#GENERATE DIAGONAL-RECTANGULAR PAIR OF COLORED MATRICES

#Make a binary riley matrix (looks like a checkerboard of 0's and 1's)
rect_checkerboard_matrix=messengers.make_rect_checkerboard(M,N)


for i in range(iterations):
	rect_color_matrix=numpy.zeros((M,N),dtype='int')

	#randomly assign colors to this from the color key defined above
	#do this by randomly choosing a color key value according to the probability weights assigned above (right now I favor white, as Riley does)
	#and then multiplying the randomly chosen value by the binary checkerboard matrix's value at each address
	color_keys=list(color_dict.keys())
	color_probabilities = [color_dict[k][1] for k in color_dict]
	for m in range(M):
		for n in range(N):
			rand_color_key = choice(color_keys,p=color_probabilities)
			rect_color_matrix[m][n] = rand_color_key*rect_checkerboard_matrix[m][n]

	print(rect_color_matrix)

	#fetch diagonal counterpart of this randomly-colored matrix
	diag_color_matrix=messengers.rect_to_diag_clockwise(rect_color_matrix)
	print(diag_color_matrix)
	
	visualizers.opencv(rect_color_matrix,'sample_%d_rect.png'%i,rect_L,r,color_dict)
	visualizers.opencv(diag_color_matrix,'sample_%d_diag.png'%i,diag_L,r,color_dict)
visualizers.fabricjs(rect_color_matrix,'sample_rect.html',rect_L,r,color_dict)
visualizers.fabricjs(diag_color_matrix,'sample_diag.html',diag_L,r,color_dict)
visualizers.text([diag_color_matrix,rect_color_matrix])


