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

    version('master',
            git='https://bitbucket.org/cactuscode/coredoc.git', branch='master')

    variant('funhpc', default=False, description='Enable FunHPC')
    variant('llvm', default=False, description='Enable LLVM')
    variant('simulationio', default=False, description='Enable SimulationIO')

    # Actual dependencies
    depends_on("blas")
    depends_on("fftw +mpi +openmp")
    depends_on("gsl")
    depends_on("hdf5 +mpi")
    depends_on("hwloc")
    depends_on("lapack")
    depends_on("lua")
    depends_on("mpi")
    depends_on("openssl")
    depends_on("papi")
    depends_on("petsc +mpi")
    depends_on("zlib")
    # TODO: Add CUDA

    depends_on("funhpc", when='+funhpc')
    depends_on("llvm", when='+llvm')
    depends_on("simulationio", when='+simulationio')

    # Configure dependencies for convenience

    # Virtual packages
    # depends_on("blas ^openblas")
    # depends_on("lapack ^openblas")
    # depends_on("mpi ^openmpi")
    depends_on("openblas")
    depends_on("openmpi")

    # Versions
    # TODO: Remove this once the latest HDF5 version is again the default
    depends_on("hdf5 @1.10.0")
    # TODO: Remove this once Spack chooses the latest 2.7 version by default
    depends_on("python @2.7.11")

    # Compilers
    cactusext_compiler = 'gcc@6.1.0-spack'
    git_compiler = cactusext_compiler
    if sys.platform == 'darwin':
        git_compiler = 'clang@7.3.0-apple'
    jemalloc_compiler = cactusext_compiler
    if sys.platform == 'darwin':
        jemalloc_compiler = 'clang@7.3.0-apple'
    python_compiler = cactusext_compiler
    if sys.platform == 'darwin':
        python_compiler = 'clang@7.3.0-apple'

    depends_on("blas %"+cactusext_compiler)
    depends_on("fftw %"+cactusext_compiler)
    depends_on("gsl %"+cactusext_compiler)
    depends_on("hdf5 %"+cactusext_compiler)
    depends_on("hwloc %"+cactusext_compiler)
    depends_on("lapack %"+cactusext_compiler)
    depends_on("lua %"+cactusext_compiler)
    depends_on("mpi %"+cactusext_compiler)
    depends_on("openssl %"+cactusext_compiler)
    depends_on("papi %"+cactusext_compiler)
    depends_on("petsc %"+cactusext_compiler)
    depends_on("zlib %"+cactusext_compiler)

    depends_on("funhpc %"+cactusext_compiler, when='+funhpc')
    depends_on("llvm %"+cactusext_compiler, when='+llvm')
    depends_on("simulationio %"+cactusext_compiler, when='+simulationio')

    # These are apparently not deduced -- why?
    depends_on("libsigsegv %"+cactusext_compiler)
    depends_on("openmpi %"+cactusext_compiler)

    git_deps = ['autoconf', 'curl', 'expat', 'openssl', 'zlib']
    depends_on("git %"+git_compiler+
               ''.join([" ^"+dep+"%"+cactusext_compiler for dep in git_deps]))
    depends_on("jemalloc %"+jemalloc_compiler, when='+funhpc')
    python_deps = ['bzip2', 'ncurses', 'readline', 'openssl', 'sqlite', 'zlib']
    depends_on("python %"+python_compiler+
               ''.join([" ^"+dep+"%"+cactusext_compiler
                        for dep in python_deps]))

    # Options
    depends_on("boost +mpi")
    # TODO: avoid ~polly ~gold
    # ~lldb ~internal_unwind ~polly ~libcxx ~compiler-rt ~gold
    depends_on("llvm", when='+llvm')
    openmpi_opts = []
    if (os.path.isfile("/usr/include/pmi.h") or
        os.path.isfile("/usr/slurm/include/pmi.h") or
        os.path.isfile("/usr/include/pmi2.h") or
        os.path.isfile("/usr/slurm/include/pmi2.h")):
        openmpi_opts.append("+pmi")
    else:
        openmpi_opts.append("~pmi")
    try:
        ibv_devices = which('ibv_devices')
        ibv_devices(output=str, error=str)
        openmpi_opts.append("+verbs")
    except:
        openmpi_opts.append("~verbs")
    depends_on("openmpi"+''.join([" "+opt for opt in openmpi_opts]))
    # TODO: Mumps doesn't build everywhere; enable it once it works
    depends_on("petsc +boost +hdf5 +mpi ~mumps")

    def install(self, spec, prefix):
        # This package does not install anything per se; it only
        # installs many of the dependencies that Cactus-based
        # applications require.
        mkdirp(prefix.lib)
