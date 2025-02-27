from mumps4py.mumps_solver import MumpsSolver

import numpy as np
from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

system = "double"
dtype = np.float32 if system == "single" else np.float64
if system in ["complex64", "complex128"]:
    dtype = np.complex64 if system == "complex64" else np.complex128

solver = MumpsSolver(verbose=False, system=system)


n = 5
irn = np.array([0,1,3,4,1,0,4,2,1,2,0,2], dtype=np.int32)
jcn = np.array([1,2,2,4,0,0,1,3,4,1,2,2], dtype=np.int32)
a = np.array([3.0,-3.0,2.0,1.0,3.0,2.0,4.0,2.0,6.0,-1.0,4.0,1.0], dtype=dtype)
b = np.array([[20.0,24.0,9.0,6.0,13.0],[20.0,24.0,9.0,6.0,13.0]], dtype=dtype)


# Split COO format indices directly across MPI processes
indices = np.arange(len(irn))  # Create index array for splitting
split_indices = np.array_split(indices, size)  # Distribute indices among processes

# Get the indices for the current process
local_indices = split_indices[rank]

# Extract local data
local_irn = irn[local_indices]
local_jcn = jcn[local_indices]
local_a = a[local_indices]

solver.set_rcd_distributed(local_irn+1, local_jcn+1, local_a)
solver.set_icntl(18,3)

if MPI.COMM_WORLD.Get_rank() == 0:
    solver.set_shape(n)
    
#Analyse 
solver.analyze()
# #Factorization Phase
solver.factorize()

#Allocation size of rhs
if MPI.COMM_WORLD.Get_rank() == 0:
    solver.set_rhs_centralized(b)

solver.solve()
if rank == 0:
    print("Solution 3", b)
    
