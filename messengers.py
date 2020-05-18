import sys
import numpy
import random
from numpy.random import choice
import time
import math





#this makes an NxM matrix of alternating zeroes and ones
def make_checkerboard(M,N):
	array = [[(i+j+1)%2 for i in range(1,N+1)] for j in range(1,M+1)]
	matrix = numpy.reshape(array,(M,N))
	print("Checkerboard\n",matrix)
	return matrix

#this makes an NxM matrix with unique values
#specifically, incrementing integers with 
def make_rectangular_matrix(M,N):
	#first have a 1x(M*N) array with the values
	array = [int((i%2)*((i+1)/2)) for i in range(1,(M*N)+1)]
	#print(array)
	#then transform into NxM matrix
	matrix = numpy.reshape(array,(M,N))
	print("Rectangular Matrix\n",matrix)
	#print(matrix)
	#worth noting that an MxN rollup is also a Riley layout
	return matrix

'''an alternative construction of the layout
creates truncated, banded matrices.

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
def transposition_indices(rect_matrix):
	
	M,N = rect_matrix.shape
	
	long_side = max(M,N)
	
	node_ids = [i for i in rect_matrix.ravel().tolist() if i!=0]
	#print(node_ids)
	
	diag_nodes = {i:[0,0] for i in node_ids}
	
	#print(nodes)
	
	diag_index = 0
	
	diag_max = 0
	
	for index in range(-long_side,long_side):
		
		O = rect_matrix.diagonal(index)
		P = numpy.flip(rect_matrix,0).diagonal(index)
		if (O.size!=0 and numpy.sum(O)!=0) or (P.size!=0 and numpy.sum(P)!=0):
			
			if P.size>diag_max:
				diag_max = P.size
			if O.size>diag_max:
				diag_max = O.size
			#print(O)
			#print(P)
			
			for o in O:
				diag_nodes[o][1]=diag_index
			for p in P:
				diag_nodes[p][0]=diag_index
			
			diag_index +=1
	
	rect_nodes = {}
	
	for m in range(M):
		for n in range(N):
			id = rect_matrix[m][n]
			if id !=0:
				rect_nodes[id]=[m,n]
	
	RT = numpy.zeros((M,N,2),dtype=int)
	DT = numpy.zeros((diag_index,diag_index,2),dtype=int)
	#print(RT.shape)
	#print(DT.shape)
		
	for id,coords in diag_nodes.items():
		
		o,p=coords
		
		m,n = rect_nodes[id]
		
		DT[o][p] = (m,n)
	
	for id,coords in rect_nodes.items():
		
		m,n=coords
		o,p=diag_nodes[id]
		
		RT[m][n] = (o,p)
	
	
	#diag_matrix = diag_matrix[~(diag_matrix==0).all(1)]
	#diag_matrix = diag_matrix[~(diag_matrix==0).all(0)]
	
	
	return RT,DT

#Takes an input matrix and a "transformation matrix" of the same dimension
#which is an array of addresses from matrix AB to matrix IJ, as given in "transposition indices" function above
#A,B is input dimensions, I,J is output dimensions
def transform(input_matrix,transform_coords,A,B,I,J):
	
	#print(input_matrix)
	#print(transform_coords)
	transformed=numpy.zeros((I,J),dtype=int)
	
	for a in range(A):
		for b in range(B):
			v=input_matrix[a][b]
			i,j=transform_coords[a][b]
			transformed[i][j]=v
	return transformed





#This function, deprecated, will take a rectangular matrix and actually transform it into its 45-degree-rotated counterpart
def diagonally_transpose(rect_matrix):
	
	M,N = rect_matrix.shape
	
	long_side = max(M,N)
	
		
	
	node_ids = [i for i in rect_matrix.ravel().tolist() if i!=0]
	#print(node_ids)
	
	nodes = {i:[0,0] for i in node_ids}
	
	#print(nodes)
	
	diag_index = 0
	
	diag_max = 0
	
	for index in range(-long_side,long_side):
		
		O = rect_matrix.diagonal(index)
		P = numpy.flip(rect_matrix,0).diagonal(index)
		if (O.size!=0 and numpy.sum(O)!=0) or (P.size!=0 and numpy.sum(P)!=0):
			
			if P.size>diag_max:
				diag_max = P.size
			if O.size>diag_max:
				diag_max = O.size
			#print(O)
			#print(P)
			
			for o in O:
				nodes[o][1]=diag_index
			for p in P:
				nodes[p][0]=diag_index
			
			diag_index +=1
	
	diag_matrix = numpy.zeros((diag_index,diag_index),dtype=int)

	#print(diag_matrix)

	for id,coords in nodes.items():
		
		o,p=coords
		
		diag_matrix[o][p] = id
	
	
	#diag_matrix = diag_matrix[~(diag_matrix==0).all(1)]
	#diag_matrix = diag_matrix[~(diag_matrix==0).all(0)]
	
	
	print("Diagonal/Truncated-Banded Matrix\n",diag_matrix)
	return diag_matrix
	

#takes an NxM Riley checkerboard matrix, with its null entries
#returns a dictionary of nodes and neighbors (so, no null entries) with minimal attributes (neighbor_ids and self_address)
#but addresses are still implicitly based on the null-entried matrix
def make_rectangular_neighbor_dictionary(matrix):
	M,N=matrix.shape
	neighbor_dictionary ={}
	for m in range(M):
		for n in range(N):
			id = matrix[m][n]
			if id!=0:
				neighbor_ids = [matrix[i][j] for (i,j) in [(m+1,n+1),(m-1,n+1),(m+1,n-1),(m-1,n-1)] if i>=0 and i<M and j>=0 and j<N]
				neighbor_dictionary[id] = {'neighbor_ids':neighbor_ids,'self_address':[n,m]}
	#print(neighbor_dictionary)
	return neighbor_dictionary
	
#takes a Riley diagonal matrix, with its null entries
#returns a dictionary of nodes and neighbors (so, no null entries) with minimal attributes (neighbor_ids and self_address)
#ids are still implicitly based on the null-entried matrix
def make_diagonal_neighbor_dictionary(matrix):
	O,P=matrix.shape
	neighbor_dictionary ={}
	for o in range(O):
		for p in range(P):
			id = matrix[o][p]
			if id!=0:
				neighbor_ids = [matrix[i][j] for (i,j) in [(o+1,p),(o-1,p),(o,p+1),(o,p-1)] if i>=0 and i<O and j>=0 and j<P]
				neighbor_dictionary[id] = {'neighbor_ids':neighbor_ids,'self_address':[o,p]}
	#print(neighbor_dictionary)
	return neighbor_dictionary


#all-purpose node-altering function
#alterations to be sent as 3-ples: (node_id,attribute,new_value)
def alter_states(neighbor_dictionary,alterations):
	for alteration in alterations:
		node_id,attribute,new_value = alteration
		neighbor_dictionary[node_id][attribute] = new_value
	return neighbor_dictionary

def recalculate_connectedness(neighbor_dictionary,affected_ids):
	
	for node_id in affected_ids:
		
		node = neighbor_dictionary[node_id]
		
		neighbor_ids = node['neighbor_ids']
		
		neighbor_colors = [neighbor_dictionary[id]['color'] for id in neighbor_ids if neighbor_dictionary[id]['color']!=None]
		
		connectedness_score = len(neighbor_colors)
		
		neighbor_dictionary[node_id]['connectedness_score']=connectedness_score
	return neighbor_dictionary
	
	
	
	