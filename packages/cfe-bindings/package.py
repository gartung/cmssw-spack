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
#     spack install cfe-bindings
#
# You can edit this file again by typing:
#
#     spack edit cfe-bindings
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class CfeBindings(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://releases.llvm.org/3.8.0/cfe-3.8.0.src.tar.xz"

    version('3.8.0', 'cc99e7019bb74e6459e80863606250c5')

    def install(self, spec, prefix):
        cp=which('cp')
        mkdirp('%s' % self.prefix.lib)
        mkdirp('%s' % self.prefix.include)
        mkdirp('%s' % self.prefix.bin)
        mkdirp(self.prefix.lib+'/python2.7/site-packages/clang')
        cp('-rpv','/usr/local/Cellar/llvm/4.0.1/lib/python2.7/site-packages/clang/',self.prefix.lib+'/python2.7/site-packages/clang/')
        cp('-rpv','/usr/local/Cellar/llvm/4.0.1/lib/libclang.dylib',self.prefix.lib)
        cp('-rpv','/usr/local/Cellar/llvm/4.0.1/bin/clang',self.prefix.bin)
    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LLVM_BASE', self.prefix)

