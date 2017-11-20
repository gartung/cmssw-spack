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


class Libuuid(AutotoolsPackage):
    """Portable uuid C library"""

    homepage = "http://sourceforge.net/projects/libuuid/"
    url      = "http://downloads.sourceforge.net/project/libuuid/libuuid-1.0.3.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Flibuuid%2F&ts=1433881396&use_mirror=iweb"

    version('1.0.3', 'd44d866d06286c08ba0846aba1086d68')

    def write_scram_toolfile(self,contents,filename):
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

        fname='libuuid.xml'
        template=Template("""<tool name="libuuid" version="$VER">
  <lib name="uuid"/>
  <client>
    <environment name="LIBUUID_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBUUID_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBUUID_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

