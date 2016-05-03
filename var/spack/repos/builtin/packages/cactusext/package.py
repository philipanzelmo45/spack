from spack import *

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

    version('master', git='00b516f4704d4a7cb50a1d97e6e8e15b', branch='master')

    variant('funhpc', default=False, description='Enable FunHPC')

    depends_on("blas")
    depends_on("fftw")
    depends_on("gsl")
    depends_on("hdf5")
    depends_on("hwloc")
    depends_on("lapack")
    depends_on("lua")
    depends_on("mpi")
    depends_on("openssl")
    depends_on("papi")
    depends_on("petsc")
    depends_on("zlib")

    depends_on("funhpc", when='+funhpc')

    def install(self, spec, prefix):
        # This package does not install anything per se; it only
        # installs many of the dependencies that Cactus-based
        # applications require.
        mkdir(prefix.lib)
