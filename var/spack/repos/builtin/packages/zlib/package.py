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


class Zlib(AutotoolsPackage):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    homepage = "http://zlib.net"
    url = "http://zlib.net/fossils/zlib-1.2.10.tar.gz"

    version('1.2.11', '1c9f62f0778697a09d36121ead88e08e')
    # The web site says:
    # Due to the bug fixes, any installations of 1.2.9 or 1.2.10
    # should be immediately replaced with 1.2.11.
    # version('1.2.10', 'd9794246f853d15ce0fcbf79b9a3cf13')
    version('1.2.8', '44d667c142d7cda120332623eab69f40')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    def setup_environment(self, spack_env, run_env):
        if '+pic' in self.spec:
            spack_env.set('CFLAGS', self.compiler.pic_flag)
