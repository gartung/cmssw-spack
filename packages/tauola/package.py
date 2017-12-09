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
# You should have received a copy of th GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import glob
import os
import shutil
import distutils.dir_util as du

class Tauola(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola/tauola-28.121.2-x86_64-slc6-gcc46-opt.tgz"

    version('28.121.2', '2f3665b7c332212f0dfe6db5cb9ad94261bb389086fa44b9f03c419f3e6e09b9')

    depends_on('pythia6')
    depends_on('photos')


    def install(self, spec, prefix):
        with working_dir(str(self.version)):
            du.copy_tree('x86_64-slc6-gcc46-opt',prefix)

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

        fname = 'tauola.xml'
        template = Template("""
<tool name="tauola" version="${VER}">
  <lib name="pretauola"/>
  <lib name="tauola"/>
  <client>
    <environment name="TAUOLA_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$TAUOLA_BASE/lib"/>
  </client>
  <use name="f77compiler"/>
  <use name="tauola_headers"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'tauola_headers.xml'
        template = Template("""
<tool name="tauola_headers" version="${VER}">
  <client>
    <environment name="TAUOLA_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$TAUOLA_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
