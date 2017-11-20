##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Fftjet(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/fftjet/1.5.0/fftjet-1.5.0.tar.gz"

    version('1.5.0', '9f91b6974c00ba546833c38d5b3aa563')

    depends_on('fftw')

    def configure_args(self):
        args = ['--disable-dependency-tracking',
                '--enable-threads',
                'CFLAGS=-fpic',
                'DEPS_CFLAGS=-I%s' % self.spec['fftw'].prefix.include,
                'DEPS_LIBS="-L%s -lfftw3"' % self.spec['fftw'].prefix.lib]
        return args
