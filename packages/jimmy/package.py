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


class Jimmy(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/jimmy/jimmy-4.2-slc4_amd64_gcc34.tgz"

    version('4.2', '0a1885b9c3a5191b1e8fad34a0577966')

    depends_on('herwig')

    def install(self, spec, prefix):
        with working_dir(join_path(self.version,'slc4_amd64_gcc34')):
            install_tree('include',prefix.include)
            install_tree('lib',prefix.lib)

    def url_for_version(self,version):
        url='http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/jimmy/jimmy-%s-slc4_amd64_gcc34.tgz'%version
        return url

    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def write_scram_toolfiles(self):
        """Create contents of scram tool config files for this package."""
        from string import Template
        import sys
        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'jimmy.xml'
        template = Template("""
<tool name="jimmy" version="${VER}">
  <lib name="jimmy"/>
  <client>
    <environment name="JIMMY_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$JIMMY_BASE/lib"/>
  </client>
  <use name="f77compiler"/>
  <use name="herwig"/>
  <use name="jimmy_headers"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'jimmy_headers.xml'
        template = Template("""
<tool name="jimmy_headers" version="${VER}">
  <client>
    <environment name="JIMMY_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$JIMMY_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

