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


class Magma(Package):
    """Matrix Algebra on GPU and Multicore Architectures

    The MAGMA project aims to develop a dense linear algebra library
    similar to LAPACK but for heterogeneous/hybrid architectures,
    starting with current "Multicore+GPU" systems."""

    homepage = "http://icl.cs.utk.edu/magma/index.html"
    url      = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-2.1.0.tar.gz"

    version('2.1.0', '2c4ac834e38e8bb281a7ca4751df62a6')
    version('2.0.2', '2604dd092df4ee3d790e9e979e184993')
    version('2.0.1', '6732465e13d88419a77cb5f8ccecd1fb')
    version('2.0.0', '91339efc93ccb2be630da7690a4f751b')
    version('1.7.0', '482b24d3aff54a44791cf41dd1473939')

    depends_on('cmake', type='build')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)

            make()
            make('install')
