#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:08:37 2025

@author: kissami
"""

import numpy as np
from mpi4py import MPI
from scipy.sparse import coo_matrix


rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

from mumps4py.mumps_solver import MumpsSolver


system = "double"
dtype = np.float32 if system == "single" else np.float64
if system in ["complex64", "complex128"]:
    dtype = np.complex64 if system == "complex64" else np.complex128
    
solver = MumpsSolver(verbose=False, system=system)

solver = MumpsSolver(system="double")

A = coo_matrix(([1.0, 2.0, 3.0, 4.0], ([0, 1, 2, 3], [0, 1, 2, 3])), shape=(4, 4))

solver.set_coo_centralized(A)

rhs = np.array([1.0, 2.0, 3.0, 4.0])
solver.set_rhs_centralized(rhs)

# Analyze and Factorize
solver.analyze()
solver.factorize()
solver.solve()

print("Solution is:", rhs)