from spack import *
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
    variant('simulationio', default=False, description='Enable SimulationIO')

    # Actual dependencies
    depends_on("blas")
    depends_on("fftw +mpi")
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

    depends_on("funhpc", when='+funhpc')
    depends_on("simulationio", when='+simulationio')

    # Configure dependencies for convenience
    cactusext_compiler = 'gcc@5.3.0-spack'
    jemalloc_compiler = cactusext_compiler
    if sys.platform == 'darwin':
        jemalloc_compiler = 'clang@7.3.0-apple'
    python_compiler = cactusext_compiler
    if sys.platform == 'darwin':
        python_compiler = 'clang@7.3.0-apple'

    depends_on("blas ^openblas")
    depends_on("boost +mpi")
    depends_on("hdf5 @1.10.0 +mpi")
    depends_on("jemalloc %"+jemalloc_compiler)
    depends_on("lapack ^openblas")
    depends_on("mpi ^openmpi")
    openmpi_opts = []
    try:
        ibv_devinfo = which('ibv_devinfo')
        ibv_devinfo()
        openmpi_opts.append("+verbs")
    except:
        pass
    depends_on("openmpi"+''.join([" "+opt for opt in openmpi_opts]))
    depends_on("petsc +boost +hdf5 +mpi ~mumps")
    python_deps = ['bzip2', 'ncurses', 'readline', 'openssl', 'sqlite', 'zlib']
    depends_on("python %"+python_compiler+
               ''.join([" ^"+dep+"%"+cactusext_compiler
                        for dep in python_deps]))

    def install(self, spec, prefix):
        # This package does not install anything per se; it only
        # installs many of the dependencies that Cactus-based
        # applications require.
        mkdirp(prefix.lib)
