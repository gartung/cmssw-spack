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
import glob
import os

class Photos(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "http://cern.ch/service-spi/external/MCGenerators/distribution/photos/photos-215.5-src.tgz"

    version('215.5', '87bc3383562e2583edb16dab8b2b5e30')

    patch('photos-215.5-update-configure.patch')


    def install(self, spec, prefix):
        args = ['--enable-static',
                '--disable-shared',
                '--lcgplatform=slc_amd64_gcc']
        with working_dir(str(spec.version)):
            configure(*args)
            make()
            install_tree('include',prefix.include)
            mkdirp(prefix.lib)
            for f in glob.glob('lib/archive/*'):
                install(f,join_path(prefix.lib,os.path.basename(f)))


    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc+'/scram.d/'+filename,'w') as f:
            f.write(contents)
            f.close()


    @run_after('install')
    def write_scram_toolfiles(self):
        """Create contents of scram tool config files for this package."""
        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values={}
        values['VER']=self.spec.version
        values['PFX']=self.spec.prefix

        fname='photos.xml'
        template=Template("""
<tool name="photos" version="${VER}">
  <lib name="photos"/>
  <client>
    <environment name="PHOTOS_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PHOTOS_BASE/lib"/>
  </client>
  <use name="photos_headers"/>
  <use name="f77compiler"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

        fname='photos_headers.xml'
        template=Template("""
<tool name="photos_headers" version="${VER}">
  <client>
    <environment name="PHOTOS_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$PHOTOS_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

