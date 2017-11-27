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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install castor
#
# You can edit this file again by typing:
#
#     spack edit castor
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import glob

class Castor(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://castorold.web.cern.ch/castorold/DIST/CERN/savannah/CASTOR.pkg/2.1.16-*/2.1.16-13/castor-2.1.16-13.tar.gz"

    version('2.1.16-13', '5a2cf6992ac4c1a2dcf7eb90e14233e5')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def install(self, spec, prefix):
        source_directory = self.stage.source_path
        mkdirp('%s' % prefix.include)
        mkdirp('%s/shift' % prefix.include)
        mkdirp(prefix.lib)
        mkdirp(prefix.bin)

        install('%s/h/shift.h' % source_directory,prefix.include)
        for file in glob.glob('%s/h/*' % source_directory): 
           f = join_path(source_directory,'h',file)
           install(f, '%s/shift' % prefix.include)

    def write_scram_toolfile(self,contents,filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc+'/scram.d/'+filename,'w') as f:
            f.write(contents)
            f.close()


    @run_after('install')
    def write_scram_toolfiles(self):
        """Create contents of scram tool config files for this package."""
        from string import Template
        import sys
        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values={}
        values['VER']=self.spec.version
        values['PFX']=self.spec.prefix

        fname='castor_header.xml'
        template=Template("""
<tool name="castor_header" version="${VER}">
  <client>
    <environment name="CASTOR_HEADER_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$CASTOR_HEADER_BASE/include"/>
    <environment name="INCLUDE" default="$$CASTOR_HEADER_BASE/include/shift"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$CASTOR_HEADER_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$CASTOR_HEADER_BASE/include/shift" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

        fname='castor.xml'
        template=Template("""
<tool name="castor" version="${VER}">
  <lib name="shift"/>
  <lib name="castorrfio"/>
  <lib name="castorclient"/>
  <lib name="castorcommon"/>
  <client>
    <environment name="CASTOR_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CASTOR_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$CASTOR_BASE/bin" type="path"/>
  <use name="castor_header"/>
  <use name="libuuid"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)
