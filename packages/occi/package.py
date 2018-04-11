##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import sys
import shutil

class Occi(Package):
    """An ABI hack to occi.h with std=c++17"""

    homepage = "https://github.com/cms-sw"
    url = "https://github.com/cms-sw/cms_oracleocci_abi_hack.git"

    version('1.0.0', git = "https://github.com/cms-sw/cms_oracleocci_abi_hack.git", 
             commit='88b2a965305226df1822a14af8fe7174ee5f1614')

    depends_on('oracle')

    def install(self, spec, prefix):
        make()
        with working_dir('build', create=False):
            shutil.copytree('lib',prefix.lib)
            shutil.copytree('include',prefix.include)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('INCLUDE_DIR','%s' % self.spec['oracle'].prefix.include)
        spack_env.set('LIB_DIR', '%s' % self.spec['oracle'].prefix.lib)

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

        fname = 'cms-occi.xml'
        template = Template("""
<tool name="oracleocci" version="${VER}">
  <lib name="cms_oracleocci_abi_hack"/>
  <use name="oracleocci-official"/>
  <client>
    <environment name="ORACLEOCCI_BASE" default="${PFX}"/>
    <environment name="INCLUDE" value="${PFX}/include"/>
    <environment name="LIBDIR" value="${PFX}/lib"/>
  </client>
  <runtime name="CMS_ORACLEOCCI_LIB" value="$$LIBDIR/libcms_oracleocci_abi_hack.so"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
