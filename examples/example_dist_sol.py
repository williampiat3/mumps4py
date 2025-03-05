#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:23:15 2025

@author: kissami
"""

from mumps4py.mumps_solver import MumpsSolver
import numpy as np
from mpi4py import MPI

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define the system type
system = "double"
dtype = np.float32 if system == "single" else np.float64
if system in ["complex64", "complex128"]:
    dtype = np.complex64 if system == "complex64" else np.complex128

# Initialize MUMPS solver
solver = MumpsSolver(verbose=False, system=system)

# Define matrix in coordinate format (COO)
n = 5
irn = np.array([0,1,3,4,1,0,4,2,1,2,0,2], dtype=np.int32) + 1
jcn = np.array([1,2,2,4,0,0,1,3,4,1,2,2], dtype=np.int32) + 1
a = np.array([3.0,-3.0,2.0,1.0,3.0,2.0,4.0,2.0,6.0,-1.0,4.0,1.0], dtype=dtype)

# Define the right-hand side (RHS)
b = np.array([20.0,24.0,9.0,6.0,13.0], dtype=dtype)

# Split COO format indices directly across MPI processes
indices = np.arange(len(irn))  # Create index array for splitting
split_indices = np.array_split(indices, size)  # Distribute indices among processes

# Get the indices for the current process
local_indices = split_indices[rank]

# Extract local data
local_irn = irn[local_indices]
local_jcn = jcn[local_indices]
local_a = a[local_indices]

# Set ICNTL(18) BEFORE setting the matrix (important!)
solver.set_icntl(18, 3)  # Enable distributed assembly

# Set the matrix (distributed format)
solver.set_rcd_distributed(local_irn, local_jcn, local_a, n)

# Set ICNTL(21) BEFORE factorization
solver.set_icntl(21, 1)  # Enable distributed solution

# Analyze and factorize
solver.analyze()
solver.factorize()

# Set RHS only on rank 0
if rank == 0:
    solver.set_rhs_centralized(b)

# Enable distributed solution
solver.enable_distributed_solution(1)

# Solve the system
solver.solve()

# Example usage
shape = b.shape  # Define the expected shape
dtype = np.float64  # Define the expected data type

# Convert back to NumPy array
distributed_solution = solver.pointer_to_numpy(solver.struct.sol_loc, dtype, shape)
print("Distributed solution :", distributed_solution)


print("")
isol_indices = solver.pointer_to_numpy(solver.struct.isol_loc, np.int32, b.shape)
print("Solution indices :", isol_indices)


print("")
# Construct the final sorted solution
final_solution = np.zeros(n, dtype=dtype)
final_solution[isol_indices - 1] = distributed_solution  # Sort by ISOL_loc indices
print("Final solution :", final_solution)