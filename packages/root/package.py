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

from spack import *
import sys


class Root(CMakePackage):
    """ROOT is a data analysis framework."""
    homepage = "https://root.cern.ch"
    url      = "https://root.cern.ch/download/root_v6.07.02.source.tar.gz"
    # Development versions
    version('6.11.02', '95e5705e203a5e0e70be7849c915f732')

    # Production versions
    version('6.10.08', '48f5044e9588d94fb2d79389e48e1d73', preferred=True)

    depends_on('cmake@3.4.3:', type='build')
    depends_on('pkg-config',   type='build')
    depends_on("pcre")
    depends_on("fftw")
    depends_on("python+shared")
    depends_on("gsl")
    depends_on("libxml2+python^python+shared")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("giflib")
    depends_on("xz")
    depends_on("openssl")
    depends_on("xrootd")
    depends_on("freetype")

    def cmake_args(self):
        libext='so'
        if sys.platform == 'darwin':
            libext='dylib'
        pyvers=str(self.spec['python'].version).split('.')
        pyver=pyvers[0]+'.'+pyvers[1]
        options=[ '-Dcxx17=on'
                 ,'-Droofit=on'
                 ,'-Dx11=on'
                 ,'-Dminuit2=on'
                 ,'-DPCRE_CONFIG_EXECUTABLE=%s/bin/pcre-config' %
                   self.spec['pcre'].prefix
                 ,'-DPCRE_INCLUDE_DIR=%s/include' %
                   self.spec['pcre'].prefix
                 ,'-DPCRE_PCRE_LIBRARY=%s/lib/libpcre.%s' %
                  (self.spec['pcre'].prefix,libext)
                 ,'-DPCRE_PCREPOSIX_LIBRARY=%s/lib/libpcreposix.%s' %
                  (self.spec['pcre'].prefix,libext)
                 ,'-DLZMA_DIR=%s' %
                   self.spec['xz'].prefix
                 ,'-DLZMA_INCLUDE_DIR=%s/include' %
                   self.spec['xz'].prefix
                 ,'-DLZMA_LIBRARY=%s/lib/liblzma.%s' %
                  (self.spec['xz'].prefix,libext)
                 ,'-DXROOTD_ROOT_DIR=%s' %
                   self.spec['xrootd'].prefix
                 ,'-DPNG_INCLUDE_DIR=%s/include' %
                   self.spec['libpng'].prefix
                 ,'-DPNG_LIBRARY=%s/lib/libpng.%s' %
                  (self.spec['libpng'].prefix,libext)
                 ,'-DPYTHON_EXECUTABLE=%s/python' %
                  (self.spec['python'].prefix.bin)
                 ,'-DPYTHON_INCLUDE=%s' %
                  (self.spec['python'].prefix.include)
                 ,'-DPYTHON_LIBRARY=%s/libpython%s.%s' %
                  (self.spec['python'].prefix.lib,pyver,libext) ]               
        if sys.platform == 'darwin':
            darwin_options = [
                '-Dx11=off',
                '-Dcocoa=on',
                '-Dbonjour=on',
                '-Dcastor=OFF',
                '-Drfio=OFF',
                '-Ddcache=OFF']
            options.extend(darwin_options)

        return options

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('ROOTSYS', self.prefix)
        run_env.set('ROOT_VERSION', 'v6')
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
        run_env.set('ROOT_TTREECACHE_SIZE', '0')
        run_env.set('ROOT_TTREECACHE_PREFILL','0')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('ROOTSYS', self.prefix)
        spack_env.set('ROOT_VERSION', 'v6')
        spack_env.prepend_path('PYTHONPATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('ROOTSYS', self.prefix)
        run_env.set('ROOT_VERSION', 'v6')
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.set('ROOT_TTREECACHE_SIZE', '0')
        run_env.set('ROOT_TTREECACHE_PREFILL','0')

    def url_for_version(self, version):
        """Handle ROOT's unusual version string."""
        return "https://root.cern.ch/download/root_v%s.source.tar.gz" % version
