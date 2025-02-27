
# MUMPS4PY  
Python Interface for the MUMPS Solver  

## Overview  
MUMPS4PY is a Python wrapper for the **MUltifrontal Massively Parallel Solver (MUMPS)**, enabling efficient sparse matrix computations with parallel processing. It provides a high-performance interface for solving sparse linear systems using **MPI-based parallelism**.  

## Dependencies  
To use MUMPS4PY, you need:  
- **MUMPS** (compiled with shared libraries)  
- **MPI** (`mpich` or `openmpi`)  
- **Python** 3.5+  
- **NumPy**, **mpi4py**, and **SciPy**  

### Installing Dependencies (Linux)  
```bash
sudo apt install libmumps-seq-dev libmumps-dev libscotch-dev libopenmpi-dev
pip install numpy mpi4py scipy
```

## Environment Variables

| Variable       | Description | 
|----------------|------------------------------------------------------------------------|
| MUMPS_INC      | Path to the MUMPS include directory (e.g., ``dmumps_c.h``)             |
| MUMPS_INC      |  Path to the MUMPS library directory (e.g., ``libdmumps.so``)          |   
| MUMPS_SOLVERS  | Specify which MUMPS solver to use (``dmumps, cmumps, smumps, zmumps``) | 

### Example Setup:

```bash
export MUMPS_INC="/path/to/MUMPS/include"
export MUMPS_LIB="/path/to/MUMPS/lib"
export MUMPS_SOLVERS="dmumps"
```

#### You can use all mumps solvers:

```bash
export MUMPS_SOLVERS="dmumps,cmumps,zmumps,smumps"
```

### To make this permanent:

```bash
echo 'export MUMPS_INC="/path/to/MUMPS/include"' >> ~/.bashrc
echo 'export MUMPS_LIB="/path/to/MUMPS/lib"' >> ~/.bashrc
echo 'export MUMPS_SOLVERS="dmumps"' >> ~/.bashrc
source ~/.bashrc
```
## Installation

### Clone and build:

```bash
git clone https://github.com/imadki/mumps4py.git
cd mumps4py
python setup.py build_ext --inplace

```
### Install globaly

```bash
pip install .
```

## Testing the Installation

### To verify that MUMPS4PY is installed correctly:

```bash
import mumps4py.mumps_solver as mps
solver = mps.MumpsSolver(verbose=True, system="double")
print("MUMPS Solver Initialized:", solver)
```

## Running Tests

### Run pytest to validate the installation:

```bash
pytest tests/
```

### Example output:

```bash
tests/test_cmumps.py s  [25%]
tests/test_dmumps.py .  [50%]
tests/test_smumps.py s  [75%]
tests/test_zmumps.py s  [100%]
```

## Cleaning Build Artifacts

```bash
python setup.py clean
```
