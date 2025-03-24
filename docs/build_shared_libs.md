# Building Shared Libraries for MUMPS 
## MUMPS < 5.6.0
This guide explains how to build shared libraries (e.g., `libdmumps.so`) from the MUMPS source code, which are required for certain Python wrappers like MUMPS4PY when dynamic linking is preferred. Shared libraries are built in addition to the static libraries (`.a` files) that MUMPS compiles by default.


### Prerequisites 
- MUMPS source code (e.g., version 5.3.1) 
- A configured `Makefile.inc` (see `Make.inc/Makefile.debian.par` for examples) 
- A C compiler (e.g., `mpicc`) that supports shared library creation 
- Dependencies like BLAS, LAPACK, and optional orderings (e.g., PORD, Scotch, METIS) configured in `Makefile.inc` 

### Overview

The MUMPS Makefile includes a `shared_libs` target that converts static libraries (e.g., `libdmumps.a`) into shared libraries (e.g., `libdmumps.so`). This process: 
1. Builds the static libraries for the desired arithmetic types (`c`, `z`, `s`, `d`). 
2. Uses the `shared_libs` rule to create `.so` files from the `.a` files. 

### Steps to Build Shared Libraries 

#### 1. Configure `Makefile.inc` to create shared library 

Ensure you have a valid `Makefile.inc` in the MUMPS root directory. For shared libraries, key variables include: 
- `OPTC`: Compiler flags (e.g., `-fPIC` for position-independent code, required for shared libraries)
- `OPTF`: Compiler flags (e.g., `-fPIC` for position-independent code, required for shared libraries)
- Example snippet for `Makefile.inc`: 

```makefile 
#Begin Optimized options
OPTF    = -O -fopenmp -fPIC
OPTL    = -O -fopenmp
OPTC    = -O -fopenmp -fPIC
```

#### 2. Build Static Libraries

```bash
make c  # For cmumps 
make z  # For zmumps 
make s  # For smumps 
make d  # For dmumps

make all # For all libs
```

#### 3. Build Shared Libraries
- Add this rule into the `Makefile` to create the shared libraries

```makefile

shared_libs: $(patsubst $(libdir)/lib%.a, $(libdir)/lib%.so, $(wildcard $(libdir)/lib*.a)) 

$(libdir)/lib%.so: $(libdir)/lib%.a 
	$(CC) -shared -o $@ -Wl,--whole-archive $< -Wl,--no-whole-archive $(LIBPAR) $(LIBBLAS) $(LORDERINGS) $(LIBOTHERS)
	@echo "$@ created successfully."
```

***Replace $(LIBPAR) by $(LIBSEQ) if you are running sequential version of MUMPS***


- Create shared libraries

```bash
make shared_libs
```

- Verify the output:

```bash
ls lib/
# Output: libdmumps.a libdmumps.so libpord.a libpord.so ...
```

## MUMPS >= 5.6.0

```bash
make dshare
```
or

```bash
make allshared
```


