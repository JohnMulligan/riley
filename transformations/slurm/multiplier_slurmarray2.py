import numpy as np
import re
from itertools import product,islice
import time
import sys
import math
import gc
import os
#sbatch --array=0-99 multiplier_slurmarray.slurm

task_id=int(sys.argv[1])
jobarray_size=int(sys.argv[2])+1

A=[[1,0,2,0,3],
	[0,4,0,5,0],
	[6,0,7,0,8]]

C=[[0,1,0,0],
	[6,4,2,0],
	[0,7,5,3],
	[0,0,8,0]]

A=np.array(A)

C=np.array(C)

valuerange=10

m,n=A.shape

sd=int(((n+1)/2)+1)

Tm=n
Tn=sd
Um=sd
Un=m

T_num_permutations=(valuerange**(Tm*Tn))
U_num_permutations=(valuerange**(Um*Un))

num_permutations=T_num_permutations*U_num_permutations



def array_permutations(m, n):
	arrays=product([i for i in range(valuerange)],repeat=m*n)
	return arrays

T=array_permutations(n,sd)

U=array_permutations(sd,m)

print("total workload size: %d permutations" %num_permutations)

print("job array size: %d processes" %jobarray_size)

print("this task index: %d" %task_id)

slice_size=int(math.floor(num_permutations/jobarray_size))
print("total workload size on this task_id: %d permutations" %slice_size)

start_idx=task_id*slice_size
end_idx=(task_id+1)*slice_size
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

s=time.time()
##THIS CRASHES IT
task_id_work_slice=islice(product(T,U),this_run_start_idx,end_idx)
print((time.time()-s)/60, "minutes")


del(T)
del(U)
gc.collect()

print("starting...")

i=0
step=1000000
st=time.time()
for task in task_id_work_slice:
	t,u=task
	T = np.array(t).reshape((n, sd))
	U = np.array(u).reshape((sd, m))
	
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

