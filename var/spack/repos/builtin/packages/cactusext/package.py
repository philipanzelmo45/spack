from spack import *
import os
import sys

class Cactusext(Package):
    """Cactus is an open source problem solving environment designed for
    scientists and engineers. Its modular structure easily enables
    parallel computation across different architectures and
    collaborative code development between different groups. Cactus
    originated in the academic research community, where it was
    developed and used over many years by a large international
    collaboration of physicists and computational scientists.
    """
    homepage = "http://www.cactuscode.org"
    url      = "https://bitbucket.org/cactuscode/coredoc.git"

    version("master",
            git="https://bitbucket.org/cactuscode/coredoc.git", branch="master")

    variant("funhpc", default=False, description="Enable FunHPC")
    variant("julia", default=False, description="Enable Julia")
    variant("llvm", default=False, description="Enable LLVM")
    variant("simulationio", default=False, description="Enable SimulationIO")

    deps = {}
    whens = {}

    # Actual dependencies
    deps["blas"] = []
    deps["boost"] = ["+mpi"]
    deps["fftw"] = ["+mpi", "+openmp"]
    deps["gsl"] = []
    deps["hdf5"] = ["+mpi"]
    deps["hwloc"] = []
    deps["lapack"] = []
    deps["lua"] = []
    deps["mpi"] = []
    deps["openssl"] = []
    deps["papi"] = []
    deps["petsc"] = ["+boost", "+hdf5", "+mpi"]
    deps["zlib"] = []
    # TODO: Add CUDA

    whens["funhpc"] = ["+funhpc"]
    whens["julia"] = ["+julia"]
    whens["llvm"] = ["+llvm"]
    whens["simulationio"] = ["+simulationio"]

    # Configure dependencies for convenience

    # Virtual packages
    deps["openblas"] = []
    deps["openmpi"] = []

    # Initialize dependencies that are mentioned below
    deps["funhpc"] = []
    deps["git"] = []
    deps["jemalloc"] = []
    deps["julia"] = []
    # deps["libsigsegv"] = []
    deps["llvm"] = []
    deps["python"] = []
    deps["simulationio"] = []

    whens["jemalloc"] = ["+funhpc"]

    # Versions
    # TODO: Remove this once the latest HDF5 version is again the default
    deps["hdf5"].append("@1.10.0")
    # TODO: Remove this once Spack chooses the latest 2.7 version by default
    deps["python"].append("@2.7.11")

    # Compilers
    cactusext_compiler = "gcc@6.1.0-spack"
    git_compiler = cactusext_compiler
    if sys.platform == "darwin":
        git_compiler = "clang@7.3.0-apple"
    jemalloc_compiler = cactusext_compiler
    if sys.platform == "darwin":
        jemalloc_compiler = "clang@7.3.0-apple"
    python_compiler = cactusext_compiler
    if sys.platform == "darwin":
        python_compiler = "clang@7.3.0-apple"

    deps["fftw"].append("%"+cactusext_compiler)
    deps["gsl"].append("%"+cactusext_compiler)
    deps["hdf5"].append("%"+cactusext_compiler)
    deps["hwloc"].append("%"+cactusext_compiler)
    deps["lua"].append("%"+cactusext_compiler)
    deps["openssl"].append("%"+cactusext_compiler)
    deps["papi"].append("%"+cactusext_compiler)
    deps["petsc"].append("%"+cactusext_compiler)
    deps["zlib"].append("%"+cactusext_compiler)

    deps["openblas"].append("%"+cactusext_compiler)
    deps["openmpi"].append("%"+cactusext_compiler)

    deps["funhpc"].append("%"+cactusext_compiler)
    deps["julia"].append("%"+cactusext_compiler)
    deps["llvm"].append("%"+cactusext_compiler)
    deps["simulationio"].append("%"+cactusext_compiler)

    # These are apparently not deduced -- why?
    # deps["libsigsegv"].append("%"+cactusext_compiler)

    deps["git"].append("%"+git_compiler)
    git_deps = ["autoconf", "curl", "expat", "openssl", "zlib"]
    deps["git"].extend(["^"+dep+" %"+cactusext_compiler for dep in git_deps])
    deps["jemalloc"].append("%"+jemalloc_compiler)
    deps["python"].append("%"+python_compiler)
    python_deps = ["bzip2", "ncurses", "readline", "openssl", "sqlite", "zlib"]
    deps["python"].extend(
        ["^"+dep+" %"+cactusext_compiler for dep in python_deps])

    # Options
    # TODO: avoid ~polly ~gold
    # ~lldb ~internal_unwind ~polly ~libcxx ~compiler-rt ~gold
    # deps["llvm", when="+llvm")
    openmpi_opts = []
    if (os.path.isfile("/usr/include/pmi.h") or
        os.path.isfile("/usr/slurm/include/pmi.h") or
        os.path.isfile("/usr/include/pmi2.h") or
        os.path.isfile("/usr/slurm/include/pmi2.h")):
        deps["openmpi"].append("+pmi")
    try:
        ibv_devices = which("ibv_devices")
        ibv_devices(output=str, error=str)
        deps["openmpi"].append("+verbs")
    except:
        pass
    # TODO: Mumps doesn't build everywhere; enable it once it works
    deps["petsc"].append("~mumps")

    # Set dependencies
    for pkg, opts in sorted(deps.iteritems()):
        try:
            when = " ".join(whens[pkg])
        except:
            when = None
        # print pkg + " " + " ".join(opts), ("when=" + when if when else "")
        depends_on(pkg + " " + " ".join(opts), when=when)

    def install(self, spec, prefix):
        # This package does not install anything per se; it only
        # installs many of the dependencies that Cactus-based
        # applications require.
        mkdirp(prefix.lib)
