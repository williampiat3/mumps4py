# MUMPS4PY Docker Setup

This document provides instructions for building and running the MUMPS4PY Docker image, which sets up a containerized environment with all necessary dependencies for development and testing.

## Building the Docker Image

- To build the Docker image from the Dockerfile in your MUMPS4PY project directory:
```bash
docker build -f Dockerfile -t mumps-test .
```

- To execute the default test suite with pytest using MPI:
```bash
docker run mumps-test
```

- To access an interactive shell inside the container:
```bash
docker run -it mumps-test bash
```
