from spack import *
import glob
import os
import shutil
import sys

class Simulationio(Package):
    """SimulationIO: Efficient and convenient I/O for large PDE simulations"""
    homepage = "https://github.com/eschnett/SimulationIO"

    version('master',
            git='https://github.com/eschnett/SimulationIO.git', branch='master')

    variant('julia', default=True)
    variant('python', default=True)

    depends_on('curl')
    depends_on('swig')

    depends_on('hdf5')
    depends_on('mpi')

    depends_on('julia', when='+julia')
    depends_on('python', when='+python')
    # depends_on('py-h5py', when='+python')
    # depends_on('py-numpy', when='+python')

    def install(self, spec, prefix):
        # Build
        make('CXX=c++',
             'HDF5_DIR=%s' % spec['hdf5'].prefix,
             'MPI_DIR=%s' % spec['mpi'].prefix,
             'PYTHON_DIR=%s' % spec['python'].prefix)

        # # Test
        # make('check')

        # Install
        shutil.rmtree(join_path(prefix, 'bin'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'include'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'lib'), ignore_errors=True)
        os.mkdir(join_path(prefix, 'bin'))
        os.mkdir(join_path(prefix, 'include'))
        os.mkdir(join_path(prefix, 'lib'))
        for binfile in ['benchmark', 'copy', 'example', 'list', 'merge',
                        'convert-carpet-output',
                        'test_RegionCalculus', 'test_SimulationIO']:
            shutil.copy(binfile, join_path(prefix, 'bin'))
        for incfile in glob.iglob('*.hpp'):
            shutil.copy(incfile, join_path(prefix, 'include'))
        for libfile in glob.iglob('*.a'):
            shutil.copy(libfile, join_path(prefix, 'lib'))
        for libfile in glob.iglob('*.dylib'):
            shutil.copy(libfile, join_path(prefix, 'lib'))
        for libfile in glob.iglob('*.so'):
            shutil.copy(libfile, join_path(prefix, 'lib'))
        for pyfile in ['H5.py', 'RegionCalculus.py', 'SimulationIO.py']:
            shutil.copy(pyfile, join_path(prefix, 'lib'))
        if sys.platform == 'darwin':
            fix_darwin_install_name(prefix.lib)