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


class Eigen(CMakePackage):
    """Eigen is a C++ template library for linear algebra matrices,
    vectors, numerical solvers, and related algorithms.
    """

    homepage = 'http://eigen.tuxfamily.org/'
    url = 'https://bitbucket.org/eigen/eigen/get/3.3.3.tar.bz2'

    version('3.3.3', 'b2ddade41040d9cf73b39b4b51e8775b')
    version('3.3.1', 'edb6799ef413b0868aace20d2403864c')
    version('3.2.10', 'a85bb68c82988648c3d53ba9768d7dcbcfe105f8')
    version('3.2.9', '59ab81212f8eb2534b1545a9b42c38bf618a0d71')
    version('3.2.8', '64f4aef8012a424c7e079eaf0be71793ab9bc6e0')
    version('3.2.7', 'cc1bacbad97558b97da6b77c9644f184')

    variant('metis', default=False, description='Enables metis backend')
    variant('scotch', default=False, description='Enables scotch backend')
    variant('fftw', default=False, description='Enables FFTW backend')
    variant('suitesparse', default=False,
            description='Enables SuiteSparse support')
    variant('mpfr', default=False,
            description='Enables support for multi-precisions FP via mpfr')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    # TODO : dependency on googlehash, superlu, adolc missing
    depends_on('metis@5:', when='+metis')
    depends_on('scotch', when='+scotch')
    depends_on('fftw', when='+fftw')
    depends_on('suite-sparse', when='+suitesparse')
    depends_on('mpfr@2.3.0:', when='+mpfr')
    depends_on('gmp', when='+mpfr')

    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def write_scram_toolfiles(self):

        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'eigen3.xml'
        template = Template("""
<tool name="eigen" version="${VER}">
  <client>
    <environment name="EIGEN_BASE"   default="${PFX}"/>
    <environment name="INCLUDE"      default="$$EIGEN_BASE/include/eigen3"/>
  </client>
  <flags CPPDEFINES="EIGEN_DONT_PARALLELIZE"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
