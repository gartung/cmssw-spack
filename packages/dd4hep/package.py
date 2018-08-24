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


class Dd4hep(CMakePackage):
    """software framework of the FCC project"""
    homepage = "https://github.com/AIDASoft/DD4hep/"
    url      = "https://github.com/AIDASoft/DD4hep/archive/v01-02.tar.gz"

    version('01.08', git='https://github.com/cms-externals/dd4hep', commit='a710edf3953bacb6a6be9e1d591df55794cf07c2')
    depends_on('cmake', type='build')
    depends_on('boost')
    depends_on('xerces-c')
    depends_on('geant4')
    depends_on('root')

    def cmake_args(self):
        spec = self.spec

        options = [
            '-DBoost_NO_BOOST_CMAKE=ON', 
            '-DDD4HEP_USE_CXX17=ON',
            '-DCMAKE_CXX_STANDARD=17',
            '-DCMAKE_BUILD_TYPE=Release',
            '-DROOTSYS=%s' % spec['root'].prefix,
            '-DDD4HEP_USE_GEANT4=ON',
            '-DDD4HEP_USE_XERCESC=ON',
            '-DXERCESC_ROOT_DIR=%s' % spec['xerces-c'].prefix
        ]

        return options

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('DD4hep_DIR', self.prefix)

    def url_for_version(self, version):
        url = "https://github.com/AIDASoft/DD4hep/archive/v{0}.tar.gz"

        return url.format(version.dashed.string)
