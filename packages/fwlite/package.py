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
from glob import glob
from string import Template
import re
import os
import fnmatch
import sys

class Fwlite(CMakePackage):
    """CMSSW FWLite"""

    homepage = "http://cms-sw.github.io"
    url      = "https://github.com/cms-sw/cmssw/archive/CMSSW_9_0_0.tar.gz"

    version('9.0.1',git='https://github.com/gartung/fwlite.git',commit='04b5af5',submodules=True)

    if sys.platform == 'darwin':
        depends_on('gcc')
        depends_on('cfe-bindings')
    depends_on('cmake')
    depends_on('root')
    depends_on('tbb')
    depends_on('tinyxml')
    depends_on('clhep')
    depends_on('md5')
    depends_on('python')
    depends_on('vdt')
    depends_on('boost')
    depends_on('libuuid')
    depends_on('libsigcpp')
    depends_on('xrootd')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite')
    depends_on('bzip2')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('libpng')
    depends_on('giflib')
    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('xz')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('bzip2')
    depends_on('castor')
    depends_on('davix')
    depends_on('fireworks-data')

    def cmake_args(self):
        args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path]
        args.append('-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix)
        args.append('-DCASTOR_INCLUDE_DIR=%s/include' % self.spec['castor'].prefix)
        args.append('-DBOOST_ROOT=%s' % self.spec['boost'].prefix)
        args.append('-DTBB_ROOT_DIR=%s' % self.spec['tbb'].prefix)
        args.append('-DTINYXMLROOT=%s' % self.spec['tinyxml'].prefix)
        args.append('-DMD5ROOT=%s' % self.spec['md5'].prefix)
        args.append('-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix)
        args.append('-DSIGCPPROOT=%s' % self.spec['libsigcpp'].prefix)
        args.append('-DDAVIXROOT=%s' % self.spec['davix'].prefix)
        return args

