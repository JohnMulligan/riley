import sys
import numpy
import random
from numpy.random import choice
import time
import math

M = int(sys.argv[1])
N = int(sys.argv[2])

#this makes an NxM matrix of alternating zeroes and ones
def make_rect_checkerboard(M,N):
	array = [[(i+j+1)%2 for i in range(1,N+1)] for j in range(1,M+1)]
	matrix = numpy.reshape(array,(M,N))
	#print("Checkerboard\n",matrix)
	return matrix

#this makes an NxM matrix with unique values
#specifically, incrementing integers with 
def make_rectangular_unique_id_matrix(M,N):
	#first have a 1x(M*N) array with the values
	array = [int((i%2)*((i+1)/2)) for i in range(1,(M*N)+1)]
	#print(array)
	#then transform into NxM matrix
	matrix = numpy.reshape(array,(M,N))
	#print("Rectangular Matrix\n",matrix)
	#print(matrix)
	#worth noting that an MxN rollup is also a Riley layout
	return matrix

'''an alternative construction of Riley's rectangular layouts produces truncated, banded matrices.

The goal is to take this:
[[1 0 2 0 3]
 [0 4 0 5 0]
 [6 0 7 0 8]]
 
And turn it into this:
[[0 1 0 0]
 [6 4 2 0]
 [0 7 5 3]
 [0 0 8 0]]
 
or this:
[[1 0 2]
 [0 3 0]
 [4 0 5]
 [0 6 0]
 [7 0 8]]
 
into this:
[[0 0 1 0]
 [0 4 3 2]
 [7 6 5 0]
 [0 8 0 0]]
 
 or this:
 [[ 1  0  2  0  3]
 [ 0  4  0  5  0]
 [ 6  0  7  0  8]
 [ 0  9  0 10  0]
 [11  0 12  0 13]]
 
 into this:
 [[0  0   1   0  0]
  [0  6   4   2  0]
  [11 9   7   5  3]
  [0  12  10  8  0]
  [0  0   13  0  0]]

there must be a more elegant way of doing this, but:'''

#This function takes a rectangular Riley matrix of any odd-integer dimensions (MxN where M,N are odd) 
#and returns a square, truncated banded Riley matrix, as though it were rotated 45 degrees right, inner spacing zeroes dropped, and buffering zeroes on the outside added
def rect_to_diag_clockwise(rect_matrix):
	M,N=rect_matrix.shape
	long_side = max(M,N)
	flipped_rect = numpy.flip(rect_matrix,0)
	
	Os=list([[i for i in flipped_rect.diagonal(idx) if i!=0] for idx in range(-long_side,long_side) if numpy.sum(flipped_rect.diagonal(idx)) != 0])
	
	O_size=P_size=len(Os)
	#print(Os)
	
	diag_matrix=numpy.zeros((O_size,P_size),dtype="int")
	
	A_buffer = list(reversed(range(1,int((M-1)/2+1))))
	B_buffer = list(reversed(range(1,int((N-1)/2+1))))
	
	left_buffer=A_buffer+[0]+list(reversed(B_buffer))
	right_buffer=B_buffer+[0]+list(reversed(A_buffer))
	
	#print(left_buffer)
	#print(right_buffer)
	
	row_idx=0
	for row in Os:		
		A=list(numpy.zeros(left_buffer[row_idx],dtype='int'))
		B=Os[row_idx]
		C=list(numpy.zeros(right_buffer[row_idx],dtype='int'))
		O=A+B+C
		diag_matrix[row_idx]=O
		row_idx+=1
	#print("diag_from_rect:\n",diag_matrix,"\n-------")
	return diag_matrix

#This function takes a square (OxP), truncated, banded matrix (one of Riley's diagonal matrices)
#and returns a rectangular Riley matrix, as though it were rotated 45 degrees left with inner spacing zeroes added
def diag_to_rect_counterclockwise(diag_matrix):
	O,P=diag_matrix.shape
	
	Ms=list(reversed([[i for i in diag_matrix.diagonal(idx) if i!=0] for idx in range(-O,O) if numpy.sum(diag_matrix.diagonal(idx)) != 0]))
		
	M=len(Ms)
	N=len(Ms[0])*2-1
	
	rect_matrix=numpy.zeros((M,N),dtype='int')
	#print(rect_matrix)
	
	row_idx=0
	for row in Ms:
		
		for col_idx in range(len(row)):
			
			if row_idx%2==0:
				n=col_idx*2
					
				m=row_idx
				
				#print(row_idx,O,M,m,n)
				
				rect_matrix[m][n] = row[col_idx]
				
				col_idx+=1
			else:
				n=col_idx*2+1
				m=row_idx
				rect_matrix[m][n] = row[col_idx]
				
		row_idx+=1
	
	#print("rect from diag:\n",rect_matrix,"\n-------")
	return rect_matrix

