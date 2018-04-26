##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Clhep(CMakePackage):
    """CLHEP is a C++ Class Library for High Energy Physics. """
    homepage = "http://proj-clhep.web.cern.ch/proj-clhep/"
    url = "http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/tarFiles/clhep-2.2.0.5.tgz"
    list_url = "https://proj-clhep.web.cern.ch/proj-clhep/"
    list_depth = 1

    version('2.4.0.0', git='https://github.com/cms-externals/clhep.git', commit='4b23da33f4607fde6f47c864871972558aa75c39')
    version('2.3.4.2', git='https://github.com/cms-externals/clhep.git', commit='03bdb22fe139303b43ca834a641f451f8e79bbcf')

    variant('cxx11', default=False, description="Compile using c++11 dialect.")
    variant('cxx14', default=True, description="Compile using c++14 dialect.")

    depends_on('cmake@2.8.12.2:', when='@2.2.0.4:2.3.0.0', type='build')
    depends_on('cmake@3.2:', when='@2.3.0.1:', type='build')

    #root_cmakelists_dir = 'CLHEP'

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if '+cxx11' in spec:
            if 'CXXFLAGS' in env and env['CXXFLAGS']:
                env['CXXFLAGS'] += ' ' + self.compiler.cxx11_flag
            else:
                env['CXXFLAGS'] = self.compiler.cxx11_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx11_flag)

        if '+cxx14' in spec:
            if 'CXXFLAGS' in env and env['CXXFLAGS']:
                env['CXXFLAGS'] += ' ' + self.compiler.cxx14_flag
            else:
                env['CXXFLAGS'] = self.compiler.cxx14_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx14_flag)

        return cmake_args

    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def write_scram_toolfiles(self):
        """Create contents of scram tool config files for this package."""
        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'clhep.xml'
        template = Template("""<tool name="clhep" version="$VER">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <lib name="CLHEP"/>
  <client>
    <environment name="CLHEP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$CLHEP_BASE/lib"/>
    <environment name="INCLUDE" default="$$CLHEP_BASE/include"/>
  </client>
  <runtime name="CLHEP_PARAM_PATH" value="$$CLHEP_BASE"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$CLHEP_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'clhepheader.xml'
        template = Template("""<tool name="clhepheader" version="$VER">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <client>
    <environment name="CLHEPHEADER_BASE" default="$PFX"/>
    <environment name="INCLUDE"    default="$$CLHEPHEADER_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
