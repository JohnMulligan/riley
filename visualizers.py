import sys
import numpy
import random
from numpy.random import choice
import cv2
import time
import re
import math
import messengers


#interesting chromatic discrepancy btw html and png outputs
#structure is maintained but color palettes are swapped.
#white is maintained (4=4)
#green is maintained (2=2)
#purple and salmon are swapped: 3 in png is 1 in html
#this may have something to do with the way she chose her colors:
##she used a harmony/complementarity formula with a "triadic" structure
###in other words those coordinates may be getting rendered in different ways but still spitting out similar-looking colors!


def opencv(matrix,fname,l,r,color_dict):
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
				R,G,B=color_dict[v][0]
				color=(B,G,R)
				img=cv2.circle(img,(x,y),r,color,-1)
	cv2.imwrite(fname,img)				


#creates a fabric.js interactive html file
def fabricjs(matrix,fname,l,r,color_dict):
	M,N=matrix.shape
	#derive the canvas size from our item layout
	#drawing a diagonal matrix, the circles have overlaps
	##I like that -- it shows the white circles as subtractions
	W=int(l*(N-1))+2*r
	H=int(l*(M-1))+2*r
	
	#print(W,H,M,N)
	
	xy_dict = {}
	
	for m in range(M):
		xy_dict[m]={}
		for n in range(N):
			val=matrix[m][n]
			if val!=0:
				x=int(n*l)
				y=int(m*l)
				
				R,G,B=color_dict[val][0]	
				color=(R,G,B)
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
	#print(colors_strings)
	
	canvas_dict = {'W':W,'H':H,'colors_array':str(colors_strings)}
		
	for canvas_prop in canvas_dict:
		canvas_txt=re.sub('\{\{%s\}\}' %canvas_prop,str(canvas_dict[canvas_prop]),canvas_txt)
	
	canvas_txt = re.sub('\{\{circles\}\}',circles_string,canvas_txt)
	
	#print(canvas_txt)
	d=open(fname,'w')
	d.write(canvas_txt)
	d.close()


##given a list of matrices, it dumps these into an output text file
def text(matrices):
	d=open('sample_matrices.txt','w')
	txt_matrices=''
	for matrix in matrices:
		M,N=matrix.shape
		for m in range(M):
			txt_matrices+=str(matrix[m])+'\n'
	#print(txt_matrices)
	d.write(txt_matrices)
	d.close()





