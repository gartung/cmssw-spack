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


class Xz(AutotoolsPackage):
    """XZ Utils is free general-purpose data compression software with
       high compression ratio. XZ Utils were written for POSIX-like
       systems, but also work on some not-so-POSIX systems. XZ Utils are
       the successor to LZMA Utils."""
    homepage = "http://tukaani.org/xz/"
    url      = "http://tukaani.org/xz/xz-5.2.0.tar.bz2"
    list_url = "http://tukaani.org/xz/old.html"

    version('5.2.3', '1592e7ca3eece099b03b35f4d9179e7c')
    version('5.2.2', 'f90c9a0c8b259aee2234c4e0d7fd70af')
    version('5.2.0', '867cc8611760240ebf3440bd6e170bb9')

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

        fname='xz.xml'
        template=Template("""<tool name="xz" version="$VER">
    <info url="http://tukaani.org/xz/"/>
    <lib name="lzma"/>
    <client>
      <environment name="XZ_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$XZ_BASE/lib"/>
      <environment name="INCLUDE" default="$$XZ_BASE/include"/>
    </client>
    <runtime name="PATH" value="$XZ_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents,fname)

