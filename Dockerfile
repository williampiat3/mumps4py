FROM ubuntu:24.04

# Installer les dépendances système (bibliothèques scientifiques et MPI)
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    gfortran cmake make \
    openmpi-bin libopenmpi-dev \
    liblapack-dev libblas-dev libatlas-base-dev \
    libscalapack-openmpi-dev \
    libmetis-dev libparmetis-dev \
    libscotch-dev libptscotch-dev \
    libmumps-ptscotch-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Variables d’environnement pour MUMPS
ENV MUMPS_SOLVERS=dmumps,cmumps,zmumps,smumps
ENV MUMPS_INC=/usr/include
ENV MUMPS_LIB=/usr/lib/x86_64-linux-gnu

# Installer les dépendances Python
RUN pip3 install build numpy scipy mpi4py pytest --break-system-packages

# Compiler et installer le package Python
RUN python3 -m build \
    && python3 -m pip install --user -e . --break-system-packages

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Commande par défaut : exécution des tests avec MPI
CMD ["mpirun", "-n", "1", "python3", "-m", "pytest", "-v"]
