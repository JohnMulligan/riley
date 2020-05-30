import sys
import numpy
import random
from numpy.random import choice
import re
import time
import math
import messengers
import json

M = int(sys.argv[1])
N = int(sys.argv[2])


#iterations = int(sys.argv[3])

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


def xy_to_canvas(matrix,fname,l):
	M,N=matrix.shape
	#derive the canvas size from our item layout
	#drawing a diagonal matrix, the circles have overlaps
	##I like that -- it shows the white circles as subtractions
	W=int(l*(N-1))+2*r
	H=int(l*(M-1))+2*r
	
	print(W,H,M,N)
	
	xy_dict = {}
	
	for m in range(M):
		xy_dict[m]={}
		for n in range(N):
			v=matrix[m][n]
			if v!=0:
				x=int(n*l)
				y=int(m*l)
				color=color_dict[v][0]
				name='node_%d_%d' %(m,n)
				xy_dict[m][n]={'x':x,'y':y,'color':'\"rgb%s\"' %str(color),'name':name,'r':r}
	
	#we have everything we need now in the above dictionary. can return a json dump, easily interpretable by javascript
	#but what follows here is a janky test-formation: write the html literals
		
	d=open('circlestemplate.txt','r')
	circles_txt=d.read()
	d.close()
	
	circles_string=''
	
	for m in xy_dict:
		for n in xy_dict[m]:
			node = xy_dict[m][n]
			circle_string = circles_txt
			for k in node:
				
				circle_string=re.sub('\{\{%s\}\}'%k,str(node[k]),circle_string)
			#print(circle_string)
			circles_string += '\n'+circle_string
	
	d=open('canvastemplate.txt','r')
	canvas_txt=d.read()
	d.close()
	
	colors_strings=[]
	for k in color_dict:
		color=color_dict[k][0]
		color_string="rgb%s" %str(color)
		colors_strings.append(color_string)
	print(colors_strings)
	
	canvas_dict = {'W':W,'H':H,'colors_array':str(colors_strings)}
		
	for canvas_prop in canvas_dict:
		canvas_txt=re.sub('\{\{%s\}\}' %canvas_prop,str(canvas_dict[canvas_prop]),canvas_txt)
	
	canvas_txt = re.sub('\{\{circles\}\}',circles_string,canvas_txt)
	
	#print(canvas_txt)
	d=open(fname,'w')
	d.write(canvas_txt)
	d.close()
	
			


	

	
#illustrate the layout in stdout
messengers.make_checkerboard(M,N)

#make rect matrix
rect_matrix = messengers.make_rectangular_matrix(M,N)
#get transformations
RT,DT=messengers.transposition_indices(rect_matrix)
O=P = len(DT[0])

iterations=1

for iteration in range(iterations):
	rect_color_matrix = numpy.zeros((M,N),dtype=int)
	
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
	
	print(rect_color_matrix)
	print(diag_color_matrix)
	
	#l is xy distance on grid between circle centers
	xy_to_canvas(rect_color_matrix,'rect.html',l=r2/math.sqrt(2))
	
	xy_to_canvas(diag_color_matrix,'diag.html',l=r2)