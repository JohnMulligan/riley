import numpy as np
import re
from itertools import product,islice
import time
import sys
import math
import os
#sbatch --array=0-99 multiplier_slurmarray.slurm

task_id=int(sys.argv[1])
jobarray_size=int(sys.argv[2])

A=[[1,0,2,0,3],
	[0,4,0,5,0],
	[6,0,7,0,8]]

C=[[0,1,0,0],
	[6,4,2,0],
	[0,7,5,3],
	[0,0,8,0]]

A=np.array(A)

C=np.array(C)

#print(C.size)

def array_permutations(m, n):
	arrays=[]
	for vals in product([0,1], repeat=m*n):
		arr = np.array(vals).reshape((m, n))
		arrays.append(arr)
	return(arrays)

T=array_permutations(5,4)

print(len(T))

U=array_permutations(4,3)

print(len(U))

TU=product(T,U)

num_permutations=(len(T)*len(U))
print("total workload size: %d permutations" %num_permutations)

print("job array size: %d processes" %jobarray_size)

print("this task index: %d" %task_id)

slice_size=int(math.floor(num_permutations/jobarray_size))
print("total worload size on this task_id: %d permutations" %slice_size)

start_idx=task_id*slice_size
end_idx=(task_id+1)*slice_size-1
this_run_start_idx=start_idx

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


task_id_work_slice=islice(TU,this_run_start_idx,end_idx)

i=0
step=1000000
st=time.time()
for task in task_id_work_slice:
	T,U=task
	B=np.dot(U,np.dot(A,T))
	if np.array_equal(B,C):
		print("+++++++")
		print(T,U)
		print("+++++++")
		d=open("match_%d.txt" %(str(i+start_idx)),"w")
		d.write(str(T)+"\n"+str(U))
		d.close()
	i+=1
	if i%step==0:
		d=open("checkpoint_%d.txt"%task_id,"a")
		d.write("\n%d" %(i+this_run_start_idx))
		d.close()
		print(i+this_run_start_idx)
		steps_per_second=i/(time.time()-st)
		print("at %d steps per second" %steps_per_second)
		estimated_time_remaining_minutes=int(((end_idx-this_run_start_idx)/steps_per_second)*60)
		print("estimated time remaining (minutes): %d" %estimated_time_remaining_minutes)

