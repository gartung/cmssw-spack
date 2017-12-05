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


class Tauolapp(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-1.1.5-src.tgz"

    version('1.1.5', '2d9a3bc7536ddc5d937bbe711ddbadbe')

    depends_on('hepmc')
    depends_on('pythia8')
    depends_on('lhapdf')
    depends_on('boost')

    def configure_args(self):
        args = ['--with-hepmc=%s' % self.spec['hepmc'].prefix,
                '--with-pythia8=%s' % self.spec['pythia8'].prefix,
                '--with-lhapdf=%s' % self.spec['lhapdf'].prefix,
                'CPPFLAGS=-I%s' % self.spec['boost'].prefix.include]
        return args

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

        fname = 'tauolapp.xml'
        template = Template("""
<tool name="tauolapp" version="${VER}">
  <lib name="TauolaCxxInterface"/>
  <lib name="TauolaFortran"/>
  <lib name="TauolaTauSpinner"/>
  <client>
    <environment name="TAUOLAPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$TAUOLAPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$TAUOLAPP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="hepmc"/>
  <use name="f77compiler"/>
  <use name="pythia8"/>
  <use name="lhapdf"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
