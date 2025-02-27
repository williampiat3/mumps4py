from mumps4py.mumps_solver import MumpsSolver

import numpy as np
from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

system = "complex64"
dtype = np.float32 if system == "single" else np.float64
if system in ["complex64", "complex128"]:
    dtype = np.complex64 if system == "complex64" else np.complex128
    
solver = MumpsSolver(verbose=False, system=system)

n = 5
irn = np.array([0,1,3,4,1,0,4,2,1,2,0,2], dtype=np.int32)
jcn = np.array([1,2,2,4,0,0,1,3,4,1,2,2], dtype=np.int32)
a = np.array([3.0,-3.0,2.0,1.0,3.0,2.0,4.0,2.0,6.0,-1.0,4.0,1.0], dtype=dtype)
b = np.array([20.0,24.0,9.0,6.0,13.0], dtype=dtype)

n = len(b)

ts = MPI.Wtime()

solver.set_shape(n)
solver.set_rcd_centralized(irn+1, jcn+1, a)

solver._mumps_call(job=1)

rhs = b.copy()

solver._mumps_call(job=2)

solver.set_rhs_centralized(rhs)
solver._mumps_call(3)

print("cpu time is ",  MPI.Wtime() - ts)




