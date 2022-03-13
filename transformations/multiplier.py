import numpy as np
from itertools import product
import time


A1=[[2,0,1,0,4],
	[0,1,0,4,0],
	[3,0,1,0,4]]

C=[[0,2,0,0],
	[3,1,1,0],
	[0,1,4,4],
	[0,0,4,0]]

A1=np.array(A1)

C=np.array(C)

print(C.size)

def array_permutations(m, n):
	arrays=[]
	for vals in product([0,1], repeat=m*n):
		arr = np.array(vals).reshape((m, n))
		arrays.append(arr)
	return(arrays)

T1as=array_permutations(5,4)

T1bs=array_permutations(4,3)

print(len(T1as),len(T1bs),"-->",len(T1as)*len(T1bs),"permutations")

i=0
step=10000000

for T1a in T1as:
	for T1b in T1bs:
		B=np.dot(T1b,np.dot(A1,T1a))
		if np.array_equal(B,C):
			print("+++++++")
			print(T1a,T1b)
			print("+++++++")
			
			d=open("match_%d.txt" %(str(i)),"w")
			d.write(str(T1a)+"\n"+str(T1b))
			d.close()
		i+=1
		if i%step==0:
			print(i)
