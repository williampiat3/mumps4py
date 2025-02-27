from mumps4py.mumps_solver import MumpsSolver

import numpy as np
from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

# Choose system type
system = "complex128"
dtype = np.float32 if system == "single" else np.float64
if system in ["complex64", "complex128"]:
    dtype = np.complex64 if system == "complex64" else np.complex128

# Initialize MUMPS solver
solver = MumpsSolver(verbose=False, system=system)

# Example matrix with 2 elements (NELT=2)
A = np.array([
    [-1,  2,  3,  0,  0],
    [ 2,  1,  1,  0,  0],
    [ 1,  1,  3, -1,  3],
    [ 0,  0,  1,  2, -1],
    [ 0,  0,  3,  2,  1]
], dtype=dtype)

n = 5  # Matrix order
nelt = 2  # Number of elements

# Element pointers (1-based, NELT+1 size)
eltptr = np.array([1, 4, 7], dtype=np.int32)  

# Element variable indices
eltvar = np.array([1, 2, 3, 3, 4, 5], dtype=np.int32)  

# Matrix values (stored by columns)
a_elt = np.array([-1, 2, 1, 2, 1, 1, 3, 1, 1, 2, 1, 3, -1, 2, 2, 3, -1, 1], dtype=dtype)

bb = np.array([1, 20, 3, 4, 5], dtype=dtype)  # Example RHS
rhs = bb.copy()

# Set MUMPS solver parameters
solver.set_icntl(5, 1)
solver.set_icntl(18, 0)

# Set elemental matrix with proper formatting
solver.set_elemental_matrix(n, nelt, eltptr, eltvar, a_elt)

solver.set_shape(n)
solver.set_rhs_centralized(bb)
solver.analyze()
solver.factorize()
solver.solve()

# Print results
if rank == 0:
    print("Solution:", bb)

print("Check solution:", A.dot(bb) - rhs)
