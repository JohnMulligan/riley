This repository contains some preliminary tools for creating matrices and graphical representations of them, based on Bridget Riley's Messengers series.

------------
messengers.py does the core, abstract work here. <br/>

It can create a binary, rectangular checkerboard matrices in Riley format:
	
	1) Binary checkerboards:
	messengers.make_rect_checkerboard(M,N)

	Will give you an MxN matrix like:
	[[1 0 1 0 1]
	[0 1 0 1 0]
	[1 0 1 0 1]]

	2) Unique ID checkerboards:
	make_rectangular_unique_id_matrix(M,N)
	Will give you an MxN matrix like:
	[[1 0 2 0 3]
	 [0 4 0 5 0]
	 [6 0 7 0 8]]

It can perform two specific but crucial transformations.<br/>
Riley's canvases as represented in the checkerboard format are inner-sparse -- zeroes every other item.<br/>
But these have corresponding, square, truncated-banded matrices that are outer-sparse -- triangular buffers of zeroes around a central band.<br/>
I therefore have 2 functions that transform: rectangular to diagonal, and diagonal to rectangular -- 45 degrees only, don't quite have the full range of motion yet.<br/>

NOTE: THESE TRANSFORMATION FUNCTIONS ONLY WORK WITH ZEROES FOR NULL ENTRIES AND NULL ENTRIES ONLY.<br/>
A ZERO IN WHAT SHOULD BE A NON-NULL ENTRY GIVEN HER LAYOUTS IS LIKELY TO BREAK IT.<br/>
So for instance in a 3-color canvas I used 4 color values (1=purple, 2=green, 3=salmon, and 4=white) even though I had a white background.<br/>
In other words, despite the white circles being indistinguishable from the white canvas, null entries were 0 and white entries were 4

	1) Inner-sparse "rectangular" matrix to outer-sparse square "diagonal" matrix by ... sort of ... rotating them clockwise 45 degrees
	rect_to_diag_clockwise(rect_matrix)
	Will take this Rectangular Matrix:
	[[2 0 1 0 4]
	 [0 1 0 4 0]
	 [3 0 1 0 4]]
	And return this Diagonal Matrix:
	[[0 2 0 0]
	 [3 1 1 0]
	 [0 1 4 4]
	 [0 0 4 0]]	

	2) Similarly, outer-sparse "diagonal" matrices can be trasformed into inner-sparse "rectangular" matrices by ... sort of ... rotating them counterclockwise 45 degrees
	Diagonal Matrix
	[[0 2 0 0]
	 [3 1 1 0]
	 [0 1 4 4]
	 [0 0 4 0]]
	Rectangular Matrix
	[[2 0 1 0 4]
	 [0 1 0 4 0]
	 [3 0 1 0 4]]

---------------------------
visualizers.py contains a few visualization functions.<br/>

In most cases, you need to pass it:<br/>
a. the matrix<br/>
b. output filename<br/>
c. basic layout information:<br/>

	l=distance between circles' radii
	r=circles' radii
	color dictionary, usually in the format of
		key:[(R,G,B),probability [optional],color_name [optional]]

		e.g.,
		color_dict={
		1:[(170,163,195),.2,'purple'],
		2:[(139,193,137),.2,'green'],
		3:[(218,181,171),.2,'salmon'],
		4:[(255,255,255),.4,'white']
		}



Use PIL to create png's out of the matrix:<br/>
visualizers.pillow(matrix,fname,l,r,color_dict)

Use Fabric.js to create (minimally for now) interactive html files with fabric.js<br/>
visualizers.fabricjs(matrix,fname,l,r,color_dict)

Use text to print out raw text representations of an array of matrices.<br/>
visualizers.text([matrix1,matrix2...])


-------------------
demo_painter.py is a test implementation of messengers.py and visualizers.py

It takes 3 parameters:<br/>
M = rectangular Riley matrix's rows (must be odd number)<br/>
N = rectangular Riley matrix's columns (must be odd number)<br/>
iterations = number of png's to create (default is 1)

Produces corresponding rectangular and diagonal Riley matrices with randomly-assigned colors.

First by generating the rectangular Riley binary checkerboard.<br/>
Then by randomly assigning colors using probability weights (hard-coded in right now as the above color dictionary).<br/>
Then by transforming that colored rectangular Riley matrix into its corresponding diagonal Riley matrix.

It generates 1 text file with all the matrices printed.

It generates 2 html files (diagonal and rectangular matrices) with fabric.js interactivity.

It generates 2 png files (diag & rect) *for every iteration*.

So:<br/>
python3 demo_painter.py 5 7 3<br/>

Generates:
	
	5x7 random-colored rectangular Riley matrix<br/>
	6x6 corresponding banded Riley matrix<br/>
	1 txt file<br/>
	2 html files<br/>
	6 png files<br/>


