This repository contains some preliminary tools for creating matrices and graphical representations of them, based on Bridget Riley's Messengers series.

messengers.py does the core, abstract work here. Its functions can generate matrices that conform to Riley's layouts, they can perform basic calculations on these matrices, and they can transform these matrices.
*calling make_rectangular_matrix(M,N) will return a rectangular MxN matrix checkerboarded with zeros.
*You should really only pass it odd integers as M,N 
For instance make_rectangular_matrix(3,5) will return:
Rectangular Matrix
 [[1 0 2 0 3]
 [0 4 0 5 0]
 [6 0 7 0 8]]

*I've found that if we accept the above as a reasonable abstraction of her canvas layouts, then matrices like the above have corresponding square, banded matrices:
Diagonal Matrix
[[0 3 0 0]
 [2 1 3 0]
 [0 4 2 4]
 [0 0 3 0]]

*My route for producing these is likely not the most efficient but it bakes in the assumption that these are symmetrical.
**First, pass the rectangular matrix to the transposition_indices function. This will return two matrices that are symmetrical-ish, with unique id's in each of the addresses and lookups to the address of the corresponding unique id in the paired matrix
**At which point, you can use these index matrices to quickly generate the corresponding matrix, going either way, using the transform function.
**So that if we apply a 4-tone color space to the schema randomly, we would get something like:
Rectangular Matrix
[[2 0 1 0 4]
 [0 1 0 4 0]
 [3 0 1 0 4]]
Diagonal Matrix
[[0 2 0 0]
 [3 1 1 0]
 [0 1 4 4]
 [0 0 4 0]]
**The advantage to this approach is that if you're interested in doing procedural generation or iteration of these canvases, you now have two symmetrical objects that you can operate on and quickly apply the changes to the other. So you could paint, flip, paint, flip, paint...


--------
There are currently two drawing functions that make use of messengers.py:
1) fabric_js_random_painter.py
--> Interactive, but barely; needs more work
--> Very lightweight, almost no dependencies
general usage: python fabric_js_random_painter.py M N
example usage: python3 fabric_js_random_painter.py 5 7
A very janky literal-writing html generator that cranks out an MxN rectangular matrix, and its corresponding diagonal matrix, with randomly-assigned colors, as html pages, drawn on an html5 canvas using fabric.js
With a little interactivity baked in (when you roll over one of the nodes it randomly changes the color (within the predefined palette). This is just a demo, it needs to be made more flexible.
Currently using a few .txt files in this repo as its page elements and then writing these out with basic string substitution.
2) opencv_random_painter.py
--> Static but scalable, portable
--> Does require the Python opencv binding, which is a massive pain to install on Linux (or at least used to be)
general usage: python opencv_random_painter.py M N X
example usage: python3 opencv_random_painter.py 5 7 10
This generates X pairs of symmetrical matrices based on an MxN rectangular matrix, with .png output files. I'm currently using it to generate my Desktop background images.


