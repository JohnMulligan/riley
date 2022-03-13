import sys
import re
import pprint
import numpy as np

#rotate an inner-sparse rectangular riley matrix A of shape m,n
#clockwise into an outers-parse square riley matrix of shape (((n+1)/2)+1),(((n+1)/2)+1)

# takes two dot products:

# U * ( A * T ) = C

# T is shape n,(((n+1)/2)+1)
# U is shape (((n+1)/2)+1),m

# this algo does destroy information
# but theoretically it shouldn't matter
#as the loss isn't greater than the sparsity of the original


def valid(x):
	try:
		x=int(x)
	except:
		print(x, "is not an integer")
		exit()
	
	if x%2 != 1:
		print("A proper Riley matrix will have an odd number of rows and columns.")
		print(x,'is not odd.')
		exit()
	
	return x

m=sys.argv[1]
n=sys.argv[2]

m=valid(m)
n=valid(n)

#square dimension formula
sd=int(((n+1)/2)+1)

A=[]
for i in range(1,m+1):
	J=[]
	for j in range(1,n+1):
		if i%2 == j%2:
			a="A%d%d" %(i,j)
		else:
			a="0"
		J.append(a)
	A.append(J)

print(	" --v-v-v-vvv-v-v-v--\n",
		"-v-v-v-v-A-v-v-v-v-\n",
		"--v-v-v-vvv-v-v-v--")


pp = pprint.PrettyPrinter(indent=4)
pp.pprint(A)


def full_matrix_address_strings(m,n,label):
	V=[]
	for i in range(1,m+1):
		J=[]
		for j in range(1,n+1):
			J.append("%s%d%d" %(label,i,j))
		V.append(J)
	return(V)

T=full_matrix_address_strings(n,sd,"T")
U=full_matrix_address_strings(sd,m,"U")
C=full_matrix_address_strings(sd,sd,"C")


print(	" --v-v-v-vvv-v-v-v--\n",
		"-v-v-v-v-T-v-v-v-v-\n",
		"--v-v-v-vvv-v-v-v--")

pp.pprint(T)


print(	" --v-v-v-vvv-v-v-v--\n",
		"-v-v-v-v-U-v-v-v-v-\n",
		"--v-v-v-vvv-v-v-v--")
		
pp.pprint(U)

print(	" --v-v-v-vvv-v-v-v--\n",
		"-v-v-v-v-C-v-v-v-v-\n",
		"--v-v-v-vvv-v-v-v--")

pp.pprint(C)









print("-------------------")
print(" U * ( A * T ) = C")
print("-------------------")


Cformulas=[]

for g in range(1,sd+1):
	H=[]
	for h in range(1,sd+1):
		
		outersum=[]
		
		for l in range(1,m+1):
			
			innersum=[]
			
			for k in range(1,n+1):
				
				if l%2 == k%2:
				
					a_address="A%d%d" %(l,k)
					b_address="T%d%d" %(k,h)
				
					addressproduct=("*".join([a_address,b_address]))
				
					addressproductstr="(%s)" %(addressproduct)
				
					innersum.append(addressproductstr)
			
			innersumstr="(%s)" %("+".join(innersum))
			
			U_address="U%d%d" %(g,l)
			
			outersum.append("%s*%s" %(U_address,innersumstr))
		
		outersumstr="%s" %("+".join(outersum))
		
		H.append(outersumstr)
			
	Cformulas.append(H)

print(	" --v-v-v-vvv-v-v-v--\n",
		"-v-v-v-v-C-v-v-v-v-\n",
		"--v-v-v-vvv-v-v-v--")
pp.pprint(Cformulas)


#print("-----------")
#print("occurrence of unique vars in each cell:")
#print("-----------")

Cvardict={}
for i in Cformulas:
	for j in i:
		Caddress="C%d%d" %(Cformulas.index(i)+1,i.index(j)+1)
		Cvardict[Caddress]={}
		vars=re.findall("[A-Z][0-9]+",j)
		for var in vars:
			if var not in Cvardict[Caddress]:
				Cvardict[Caddress][var]=1
			else:
				Cvardict[Caddress][var]+=1
			
#pp.pprint(Cvardict)





def rect_to_diag_clockwise(rect_matrix):
	M,N=[m,n]
	long_side = max(M,N)
	
	numeric_matrix=[]
	valdict={0:0}
	c=1
	for i in rect_matrix:
		J=[]
		for j in i:
			if j!="0":
				v=c
				valdict[v]=j
				c+=1
			else:
				v=0
			J.append(v)
		numeric_matrix.append(J)
	
	rect_matrix=np.array(numeric_matrix)
	
	flipped_rect = np.flip(rect_matrix,0)
	
	Os=list([[i for i in flipped_rect.diagonal(idx) if i!=0] for idx in range(-long_side,long_side) if np.sum(flipped_rect.diagonal(idx)) != 0])
	
	O_size=P_size=len(Os)
	#print(Os)
	
	diag_matrix=np.zeros((O_size,P_size),dtype="int")
	
	A_buffer = list(reversed(range(1,int((M-1)/2+1))))
	B_buffer = list(reversed(range(1,int((N-1)/2+1))))
	
	left_buffer=A_buffer+[0]+list(reversed(B_buffer))
	right_buffer=B_buffer+[0]+list(reversed(A_buffer))
	
	#print(left_buffer)
	#print(right_buffer)
	
	row_idx=0
	for row in Os:		
		A=list(np.zeros(left_buffer[row_idx],dtype='int'))
		B=Os[row_idx]
		C=list(np.zeros(right_buffer[row_idx],dtype='int'))
		O=A+B+C
		diag_matrix[row_idx]=O
		row_idx+=1
	#print("diag_from_rect:\n",diag_matrix,"\n-------")
	
	#print("///",diag_matrix)
	
	final_matrix=[]
	c=1
	for i in diag_matrix:
		J=[]
		for j in i:
			v=valdict[j]
			J.append(v)
		final_matrix.append(J)
	
	#print("--->",final_matrix)
	
	return final_matrix

squaremap=rect_to_diag_clockwise(A)

#pp.pprint(squaremap)

Cmapped=[]
Cmappeddict={}

for i in range(sd):
	J=[]
	for j in range(sd):
		Caddress="C%d%d" %(i+1,j+1)
		mappedA=str(squaremap[i][j])
		Cformula=Cformulas[i][j]
		Cmappeddict[Caddress]={"value":mappedA,"formula":Cformula}
		J.append(mappedA)
	Cmapped.append(J)

#print(Cmappeddict)



for i in range(sd):
	for j in range(sd):
		print (C[i][j],"=",Cmapped[i][j],"=",Cformulas[i][j])


