# Installing MUMPS4PY on macOS

This guide covers installing MUMPS4PY on macOS using Homebrew for dependencies.

## Prerequisites
- **Python** 3.5+ (install via [python.org](https://www.python.org/downloads/macos/) or Homebrew)
- **Homebrew**: Install from [brew.sh](https://brew.sh/)
- **MPI**: OpenMPI or MPICH via Homebrew
- **NumPy**, **mpi4py**, and **SciPy**

### Install Homebrew Dependencies
```bash
brew install open-mpi gcc libscotch
pip install numpy mpi4py scipy


## Building MUMPS on macOs
1. Download the MUMPS source from mumps-solver.org.
2. Extract the archive (e.g., MUMPS_5.6.2.tar.gz).
3. Configure and build:

```bash
cd MUMPS_5.6.2
```

4. Note the paths to include/ (for dmumps_c.h) and lib/ (for libdmumps.dylib).

```bash
export MUMPS_INC="/path/to/MUMPS_5.6.2/include"
export MUMPS_LIB="/path/to/MUMPS_5.6.2/lib"
export MUMPS_SOLVERS="dmumps"
export DYLD_LIBRARY_PATH="$MUMPS_LIB:$DYLD_LIBRARY_PATH"
```

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
