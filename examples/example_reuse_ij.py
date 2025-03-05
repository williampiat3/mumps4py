#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:23:56 2025

@author: kissami
"""
from scipy.sparse import coo_matrix
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
b = np.array([20.0,24.0,9.0,6.0,13.0], dtype=dtype)

solver.set_rcd_centralized(irn+1, jcn+1, a, n)

solver._mumps_call(job=1)

rhs = b.copy()

solver._mumps_call(job=2)

solver.set_rhs_centralized(rhs)
solver._mumps_call(3)

print("Solution:", rhs)

#Change the values of a
a = np.array([6.0,-33.0,2.0,1.0,33.0,22.0,41.0,2.0,66.0,-11.0,4.0,1.0], dtype=dtype)

# Set the data values
solver.set_data_centralized(a, n)

rhs = b.copy()

# In that case we don't need the analysis step
solver._mumps_call(job=2)

solver.set_rhs_centralized(rhs)
solver._mumps_call(3)

print("Solution:", rhs)

# Create coo matrix to check the solution
n = 5
A = coo_matrix((a, (irn, jcn)), shape=(n, n))

print("check the solution:", A.dot(rhs), b)


