Cs:{"C11":'0=U11*((A11*T11)+(A13*T31)+(A15*T51))+U12*((A22*T21)+(A24*T41))+U13*((A31*T11)+(A33*T31)+(A35*T51))',
"C12":'A11 = U11*((A11*T12)+(A13*T32)+(A15*T52))+U12*((A22*T22)+(A24*T42))+U13*((A31*T12)+(A33*T32)+(A35*T52))',
"C13":"0 = U11*((A11*T13)+(A13*T33)+(A15*T53))+U12*((A22*T23)+(A24*T43))+U13*((A31*T13)+(A33*T33)+(A35*T53))",
"C14":"0 == U11*((A11*T14)+(A13*T34)+(A15*T54))+U12*((A22*T24)+(A24*T44))+U13*((A31*T14)+(A33*T34)+(A35*T54))",
"C21":"A31 == U21*((A11*T11)+(A13*T31)+(A15*T51))+U22*((A22*T21)+(A24*T41))+U23*((A31*T11)+(A33*T31)+(A35*T51))",
"C22":"A22 == U21*((A11*T12)+(A13*T32)+(A15*T52))+U22*((A22*T22)+(A24*T42))+U23*((A31*T12)+(A33*T32)+(A35*T52))",
"C23":"A13 == U21*((A11*T13)+(A13*T33)+(A15*T53))+U22*((A22*T23)+(A24*T43))+U23*((A31*T13)+(A33*T33)+(A35*T53))",
"C24":"0 == U21*((A11*T14)+(A13*T34)+(A15*T54))+U22*((A22*T24)+(A24*T44))+U23*((A31*T14)+(A33*T34)+(A35*T54))",
"C31":"0 == U31*((A11*T11)+(A13*T31)+(A15*T51))+U32*((A22*T21)+(A24*T41))+U33*((A31*T11)+(A33*T31)+(A35*T51))",
"C32":"A33 == U31*((A11*T12)+(A13*T32)+(A15*T52))+U32*((A22*T22)+(A24*T42))+U33*((A31*T12)+(A33*T32)+(A35*T52))",
"C33":"A24 == U31*((A11*T13)+(A13*T33)+(A15*T53))+U32*((A22*T23)+(A24*T43))+U33*((A31*T13)+(A33*T33)+(A35*T53))",
"C34":"A15 == U31*((A11*T14)+(A13*T34)+(A15*T54))+U32*((A22*T24)+(A24*T44))+U33*((A31*T14)+(A33*T34)+(A35*T54))",
"C41":"0 == U41*((A11*T11)+(A13*T31)+(A15*T51))+U42*((A22*T21)+(A24*T41))+U43*((A31*T11)+(A33*T31)+(A35*T51))",
"C42":"0 == U41*((A11*T12)+(A13*T32)+(A15*T52))+U42*((A22*T22)+(A24*T42))+U43*((A31*T12)+(A33*T32)+(A35*T52))",
"C43":'A35 == U41*((A11*T13)+(A13*T33)+(A15*T53))+U42*((A22*T23)+(A24*T43))+U43*((A31*T13)+(A33*T33)+(A35*T53))',
"C44":'0 == U41*((A11*T14)+(A13*T34)+(A15*T54))+U42*((A22*T24)+(A24*T44))+U43*((A31*T14)+(A33*T34)+(A35*T54))'
}





A11=1
A12=0
A13=2
A14=0
A15=3
A21=0
A22=4
A23=0
A24=5
A25=0
A31=6
A32=0
A33=7
A34=0
A35=8





import re
import numpy as np
from itertools import product,islice
import csv
import sys
import math
import os
import time

Cname=sys.argv[1]
task_id=int(sys.argv[2])
jobarray_size=int(sys.argv[3])+1

f='A11 == U11*((A11*T12)+(A13*T32)+(A15*T52))+U12*((A22*T22)+(A24*T42))+U13*((A31*T12)+(A33*T32)+(A35*T52))'

vars=[i for i in list(set(re.findall("[A-Z][0-9]+",f))) if "A" not in i]

valrange=[i for i in range(10)]

permutations=product(valrange,repeat=len(vars))

num_permutations=len(valrange)**len(vars)

slice_size=int(math.floor(num_permutations/jobarray_size))

start_idx=task_id*slice_size
end_idx=(task_id+1)*slice_size
this_run_start_idx=start_idx

print("total workload size: %d permutations" %num_permutations)

print("job array size: %d processes" %jobarray_size)

print("this task index: %d" %task_id)

print("total workload size on this task_id: %d permutations" %slice_size)

if os.path.exists("checkpoint_%d.txt" %task_id):
	d=open("checkpoint_%d.txt" %task_id,"r")
	t=d.read()
	d.close()
	l=[i for i in t.split("\n") if re.sub("\W+","",i) !=""]
	try:
		lastline=l[-1]
		this_run_start_idx=int(lastline)
	except:
		pass
	print("work remaining on this task_id: %d" %(end_idx-this_run_start_idx))

if not os.path.exists("%s_%s.csv" %(Cname,task_id)):
	e=open("%s_%s.csv" %(Cname,task_id),"a")
	e.write(",".join([var for var in vars]))
	e.close()	
	
print(start_idx,this_run_start_idx,end_idx)

task_id_work_slice=islice(permutations,this_run_start_idx,end_idx)

c=0
d=0
step=(end_idx-start_idx)/1000
hits=0

rows=[]

st=time.time()

for p in task_id_work_slice:
	for var in vars:
		for val in p:
			exec("%s=%s" %(var,str(val)))
	if eval(f):
		rows.append(",".join([str(val) for val in p]))
		hits+=1
	c+=1
	if c-d>=step:
		d=c
		print(c)
		e=open("%s_%s.csv" %(Cname,task_id),"a")
		e.write("\n".join([row for row in rows]))
		e.close()
		e=open("checkpoint_%d.txt"%task_id,"a")
		e.write("\n%d" %(c+this_run_start_idx))
		e.close()
		rows=[]

print(time.time()-st)
		
			