#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:08:37 2025

@author: kissami
"""

import numpy as np
from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

from mumps4py.mumps_solver import MumpsSolver



system = "double"
dtype = np.float32 if system == "single" else np.float64
if system in ["complex64", "complex128"]:
    dtype = np.complex64 if system == "complex64" else np.complex128
    
solver = MumpsSolver(verbose=False, system=system)

# Define a 4x4 Sparse Matrix in 0-based indexing
n = 4  # Matrix size (4x4)
nnz = 9  # Number of non-zero entries

# Sparse Matrix Representation (COO Format, 0-based)
irn = np.array([0, 0, 1, 1, 1, 2, 2, 3, 3], dtype=np.int32)  # Row indices (0-based)
jcn = np.array([0, 1, 0, 1, 2, 1, 2, 2, 3], dtype=np.int32)  # Column indices (0-based)
a = np.array([4.0, -1.0, -1.0, 4.0, -1.0, -1.0, 4.0, -1.0, 3.0], dtype=dtype)  # Matrix values


solver.set_shape(n)
solver.set_rcd_centralized(irn+1, jcn+1, a)

# Analyze and Factorize
solver.analyze()
solver.factorize()

# Set MUMPS for sparse RHS format
solver.set_icntl(20, 1)

nz_rhs = 5  # Total non-zeros
nrhs = 2    # Number of RHS columns

rhs_values = np.array([1.1, 2.2, 3.1, 4.1, 3.2], dtype=dtype)  # Non-zero values
rhs_row_indices = np.array([1, 3, 4, 2, 3], dtype=np.int32)  # Row indices (1-based)
rhs_col_ptr = np.array([1, 4, 6], dtype=np.int32)  # Column pointers (1-based)

# Set Right Hand Side
if rank == 0:
    rhs = np.zeros((2,4))
    solver.set_rhs_centralized(rhs)

# Set the Sparse RHS in MUMPS
solver.set_rhs_sparse(rhs_values, rhs_row_indices, rhs_col_ptr, nrhs)

# Solve the system
solver.solve()


print("Solution is :", rhs)
