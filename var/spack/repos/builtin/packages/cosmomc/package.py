##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import os
import shutil


class Cosmomc(Package):
    """CosmoMC is a Fortran 2008 Markov-Chain Monte-Carlo (MCMC) engine
       for exploring cosmological parameter space, together with
       Fortran and python code for analysing Monte-Carlo samples and
       importance sampling (plus a suite of scripts for building grids
       of runs, plotting and presenting results)."""

    homepage = "http://cosmologist.info/cosmomc/"
    url      = "https://github.com/cmbant/CosmoMC/archive/Nov2016.tar.gz"

    version('Nov2016',  '98620cb746352f68fb0c1196e9a070ac', preferred=True)
    version('June2016', '92dc651d1407cca6ea9228992165f5cb')

    variant('mpi', default=True, description='Enable MPI support')
    variant('planck', default=False,
            description='Enable Planck Likelihood code and baseline data')

    patch('errorstop.patch')

    depends_on('mpi', when='+mpi')
    depends_on('planck-likelihood', when='+planck')
    depends_on('python @2.7:2.999,3.4:')

    parallel = False

    def install(self, spec, prefix):
        # Prepare
        if '+planck' in spec:
            clikdir = join_path('data', 'clik')
            try:
                os.remove(clikdir)
            except:
                pass
            os.symlink(join_path(os.environ['CLIK_DATA'], 'plc_2.0'), clikdir)

        # Build
        if '+mpi' in spec:
            wantmpi = 'BUILD=MPI'
        else:
            wantmpi = 'BUILD=NOMPI'

        # Note: Instead of checking the compiler vendor, we should
        # rewrite the Makefile to use Spack's options all the time
        if spec.compiler.name == 'gcc':
            choosecomp = 'ifortErr=1'       # choose gfortran
        elif spec.compiler.name == 'intel':
            choosecomp = 'ifortErr=0'       # choose ifort
        else:
            raise InstallError("Only GCC and Intel compilers are supported")
        
        make(wantmpi, choosecomp)

        # Install
        mkdirp(prefix.bin)
        shutil.copy(join_path('cosmomc'), prefix.bin)
        root = join_path(prefix.share, 'cosmomc')
        mkdirp(root)
        for entry in ['batch1',
                      'batch2',
                      'batch3',
                      'camb',
                      'chains',
                      'clik_latex.paramnames',
                      'clik_units.paramnames',
                      'cosmomc.cbp',
                      'data',
                      'distgeneric.ini',
                      'distparams.ini',
                      'disttest.ini',
                      'docs',
                      'job_script',
                      'job_script_MOAB',
                      'job_script_SLURM',
                      'paramnames',
                      'params_generic.ini',
                      'planck_covmats',
                      'python',
                      'scripts',
                      # don't copy 'source'
                      'test.ini',
                      'test_pico.ini',
                      'test_planck.ini',
                      'tests',
        ]:
            if os.path.isfile(entry):
                shutil.copy(entry, root)
            else:
                shutil.copytree(entry, join_path(root, entry))

    @AutotoolsPackage.sanity_check('install')
    def check_install(self):
        prefix = self.prefix
        spec = self.spec
        cosmomc = Executable(join_path(prefix.bin, 'cosmomc'))
        try:
            shutil.rmtree('spack-check')
        except:
            pass
        with working_dir('spack-check', create=True):
            for entry in [
                'camb',
                'chains',
                'data',
                'paramnames',
                'planck_covmats',
            ]:
                os.symlink(join_path(prefix.share, 'cosmomc', entry), entry)
            cosmomc(join_path(prefix.share, 'cosmomc', 'test.ini'))
            if '+planck' in spec:
                cosmomc(join_path(prefix.share, 'cosmomc', 'test_planck.ini'))
        shutil.rmtree('spack-check')
