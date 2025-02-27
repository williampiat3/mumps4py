import pytest
import os

@pytest.fixture(scope="session")
def available_solvers():
    """Detects available MUMPS solvers from the environment variable."""
    solvers = os.getenv("MUMPS_SOLVERS", "").split(",")
    return set(s.strip() for s in solvers if s.strip())
