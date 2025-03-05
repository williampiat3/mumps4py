# Installing MUMPS4PY on Windows

This guide explains how to set up MUMPS4PY on Windows. Note that Windows requires building MUMPS from source, as precompiled binaries are not widely available.

## Prerequisites
- **Python** 3.5+ (install via [python.org](https://www.python.org/downloads/) or Anaconda)
- **MPI**: Install Microsoft MPI (MS-MPI) or an alternative like MPICH
- **Git**: For cloning the repository
- **CMake**: For building MUMPS
- **Compiler**: MSVC (Visual Studio) or MinGW (e.g., via MSYS2)
- **NumPy**, **mpi4py**, and **SciPy**: Install via pip

### Install MS-MPI
1. Download and install [Microsoft MPI](https://www.microsoft.com/en-us/download/details.aspx?id=57466).
2. Add `C:\Program Files\Microsoft MPI\Bin` to your system PATH.

### Install Dependencies
```bash
pip install numpy mpi4py scipy
```

## Building MUMPS on Windows
1. Download the MUMPS source from mumps-solver.org.
2. Extract the archive (e.g., MUMPS_5.6.2.tar.gz).
3. Install a Fortran compiler (e.g., gfortran via MSYS2):

```bash
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-gcc-libfortran mingw-w64-x86_64-ninja mingw-w64-x86_64-metis mingw-w64-x86_64-scotch # If using MSYS2
```

4. Use CMake to configure and build:
```bash
cd MUMPS_5.6.2
make d
make shared_libs  # Build shared libs
```

5. Note the paths to include/ (for dmumps_c.h) and lib/ (for libdmumps.dll).

```bash
set MUMPS_INC="C:\path\to\MUMPS_5.6.2\include"
set MUMPS_LIB="C:\path\to\MUMPS_5.6.2\lib"
set MUMPS_SOLVERS="dmumps"
set PATH=%PATH%;%MUMPS_LIB%
``

## Install MUMPS4PY

1. Clone the repository:

```bash
git clone https://github.com/imadki/mumps4py.git
cd mumps4py
```

2. Build and install:

```bash
python setup.py build_ext --inplace
pip install .
```    
