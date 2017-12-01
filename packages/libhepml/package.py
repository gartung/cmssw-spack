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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install libhepml
#
# You can edit this file again by typing:
#
#     spack edit libhepml
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Libhepml(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://mcdb.cern.ch/distribution/api/libhepml-0.2.1.tar.gz"

    version('0.2.6',    'e414906a3e475cd7e5bdb6119fea15c1')
    version('0.2.5',    'c34d2155002f47de76728516a940f881')
    version('0.2.3ext', 'c17ea60f8bf93bfea7cc14bb57b0a0a1')
    version('0.2.3',    '29120e56c2bcbd59425fee82f7fdb5a1')
    version('0.2.2',    '76f3d5458252e67476dd661685e9983d')
    version('0.2.1',    '646964f8478fe0d64888514a8a1d8d19',preferred=True)

    # depends_on('foo')

    def install(self, spec, prefix):
        make()
