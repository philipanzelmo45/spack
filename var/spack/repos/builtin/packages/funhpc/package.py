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
        make('SIMFACTORY_GCC_DIR=1',
             'CXX=c++',
             'MPICXX=%s' % join_path(spec['mpi'].prefix.bin, 'mpicxx'),
             'MPIRUN=%s' % join_path(spec['mpi'].prefix.bin, 'mpirun'),
             'SIMFACTORY_CEREAL_DIR=%s' % spec['cereal'].prefix,
             'SIMFACTORY_CEREAL_CXXFLAGS=-I%s' % spec['cereal'].prefix.include,
             'SIMFACTORY_CEREAL_LDFLAGS=-L%s' % spec['cereal'].prefix.lib,
             'SIMFACTORY_CEREAL_LIBS=',
             'SIMFACTORY_HWLOC_DIR=%s' % spec['hwloc'].prefix,
             'SIMFACTORY_HWLOC_CXXFLAGS=-I%s' % spec['hwloc'].prefix.include,
             'SIMFACTORY_HWLOC_LDFLAGS=-L%s' % spec['hwloc'].prefix.lib,
             'SIMFACTORY_HWLOC_LIBS=-lhwloc',
             'SIMFACTORY_JEMALLOC_DIR=%s' % spec['jemalloc'].prefix,
             'SIMFACTORY_JEMALLOC_CXXFLAGS=-I%s' % spec['jemalloc'].prefix.include,
             'SIMFACTORY_JEMALLOC_LDFLAGS=-L%s' % spec['jemalloc'].prefix.lib,
             'SIMFACTORY_JEMALLOC_LIBS=-ljemalloc',
             'SIMFACTORY_QTHREADS_DIR=%s' % spec['qthreads'].prefix,
             'SIMFACTORY_QTHREADS_CXXFLAGS=-I%s' % spec['qthreads'].prefix.include,
             'SIMFACTORY_QTHREADS_LDFLAGS=-L%s' % spec['qthreads'].prefix.lib,
             'SIMFACTORY_QTHREADS_LIBS=-lqthread',
             'lib',
             # The selftests don't build on Comet (memory ulimit too tight?)
             # 'selftest', 'selftest-funhpc',
             'benchmark', 'benchmark2', 'fibonacci', 'hello', 'pingpong')

        # Install
        shutil.rmtree(join_path(prefix, 'bin'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'include'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'lib'), ignore_errors=True)
        os.mkdir(join_path(prefix, 'bin'))
        os.mkdir(join_path(prefix, 'include'))
        os.mkdir(join_path(prefix, 'lib'))
        for binfile in [# 'selftest', 'selftest-funhpc',
                        'benchmark', 'benchmark2', 'fibonacci', 'hello',
                        'pingpong']:
            shutil.copy(binfile, join_path(prefix, 'bin'))
        for subdir in ['adt', 'cxx', 'fun', 'funhpc', 'qthread']:
            os.mkdir(join_path(prefix, 'include', subdir))
            for incfile in glob.iglob(join_path(subdir, '*.hpp')):
                shutil.copy(incfile, join_path(prefix, 'include', subdir))
        shutil.copy('libfunhpc.a', join_path(prefix, 'lib'))
