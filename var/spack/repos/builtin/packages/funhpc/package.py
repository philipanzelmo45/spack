from spack import *
import glob
import os
import shutil

class Funhpc(Package):
    """FunHPC: Functional HPC Programming"""
    homepage = "https://bitbucket.org/eschnett/funhpc.cxx"

    version('master',
            git='https://bitbucket.org/eschnett/funhpc.cxx', branch='master')

    depends_on("cereal")
    depends_on("curl")
    depends_on("hwloc")
    depends_on("jemalloc")
    depends_on("mpi")
    depends_on("qthreads")

    def install(self, spec, prefix):
        # Build
        make('CXX=c++',
             'MPICXX=%s' % spec['mpi'].mpicxx,
             'MPIRUN=%s' % join_path(spec['mpi'].prefix.bin, 'mpirun'),
             'CEREAL_DIR=%s' % spec['cereal'].prefix,
             'HWLOC_DIR=%s' % spec['hwloc'].prefix,
             'JEMALLOC_DIR=%s' % spec['jemalloc'].prefix,
             'QTHREADS_DIR=%s' % spec['qthreads'].prefix,
             'lib',
             # The selftests don't build on Comet (memory ulimit too tight?)
             'selftest', 'selftest-funhpc',
             'benchmark', 'benchmark2',  
             'fibonacci', 'hello', 'pingpong',
        )

        # Install
        shutil.rmtree(join_path(prefix, 'bin'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'include'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'lib'), ignore_errors=True)
        os.mkdir(join_path(prefix, 'bin'))
        os.mkdir(join_path(prefix, 'include'))
        os.mkdir(join_path(prefix, 'lib'))
        for binfile in [# 'selftest', 'selftest-funhpc',
                'benchmark', 'benchmark2', 'fibonacci', 'hello', 'pingpong']:
            shutil.copy(binfile, join_path(prefix, 'bin'))
        for subdir in ['adt', 'cxx', 'fun', 'funhpc', 'qthread']:
            os.mkdir(join_path(prefix, 'include', subdir))
            for incfile in glob.iglob(join_path(subdir, '*.hpp')):
                shutil.copy(incfile, join_path(prefix, 'include', subdir))
        shutil.copy('libfunhpc.a', join_path(prefix, 'lib'))
