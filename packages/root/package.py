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


class Root(Package):
    """ROOT is a data analysis framework."""
    homepage = "https://root.cern.ch"
    url      = "https://root.cern.ch/download/root_v6.07.02.source.tar.gz"

    version('6.08.07', git='https://github.com/cms-sw/root.git',branch='cms/ff9a7c0')
    version('6.08.06', 'bcf0be2df31a317d25694ad2736df268')
    version('6.08.02', '50c4dbb8aa81124aa58524e776fd4b4b')
    version('6.06.08', '6ef0fe9bd9f88f3ce8890e3651142ee4')
    version('6.06.06', '4308449892210c8d36e36924261fea26')
    version('6.06.04', '55a2f98dd4cea79c9c4e32407c2d6d17')
    version('6.06.02', 'e9b8b86838f65b0a78d8d02c66c2ec55')

    if sys.platform == 'darwin':
        patch('math_uint.patch', when='@6.06.02')
        patch('root6-60606-mathmore.patch', when='@6.06.06')

    variant('graphviz', default=False, description='Enable graphviz support')
    variant('debug', default=False, description='debug build')

    depends_on("cmake", type='build')
#    depends_on("libtool", type='build')
    depends_on("pcre")
    depends_on("fftw~mpi")
    depends_on("graphviz", when="+graphviz")
    depends_on("python+shared")
    depends_on("gsl")
    depends_on("libxml2+python")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("giflib")
    depends_on("xz")
    depends_on("openssl")
    depends_on("xrootd")
    depends_on("freetype")

    def install(self, spec, prefix):
        libext='so'
        if sys.platform == 'darwin':
            libext='dylib'
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        options = [source_directory]
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')
        options.append('-Dcxx14=on')
        options.append('-Droofit=on')
        options.append('-Dx11=on')
        options.append('-Dminuit2=on')
        options.extend(std_cmake_args)
        options.append('-DPCRE_CONFIG_EXECUTABLE=%s/bin/pcre-config' % self.spec['pcre'].prefix)
        options.append('-DPCRE_INCLUDE_DIR=%s/include' % self.spec['pcre'].prefix)
        options.append('-DPCRE_PCRE_LIBRARY=%s/lib/libpcre.%s' % (self.spec['pcre'].prefix,libext))
        options.append('-DPCRE_PCREPOSIX_LIBRARY=%s/lib/libpcreposix.%s' % (self.spec['pcre'].prefix,libext))
        options.append('-DLZMA_DIR=%s' % self.spec['xz'].prefix)
        options.append('-DLZMA_INCLUDE_DIR=%s/include' % self.spec['xz'].prefix)
        options.append('-DLZMA_LIBRARY=%s/lib/liblzma.%s' % (self.spec['xz'].prefix,libext))
        options.append('-DXROOTD_ROOT_DIR=%s' % self.spec['xrootd'].prefix)
        options.append('-DPNG_INCLUDE_DIR=%s/include' % self.spec['libpng'].prefix)
        options.append('-DPNG_LIBRARY=%s/lib/libpng.%s' % (self.spec['libpng'].prefix,libext))
        pyvers=str(self.spec['python'].version).split('.')
        pyver=pyvers[0]+'.'+pyvers[1]
        options.append('-DPYTHON_EXECUTABLE=%s/python' % (self.spec['python'].prefix.bin))
        options.append('-DPYTHON_INCLUDE=%s' % (self.spec['python'].prefix.include))
        options.append('-DPYTHON_LIBRARY=%s/libpython%s.%s' % (self.spec['python'].prefix.lib,pyver,libext))
                       
        if sys.platform == 'darwin':
            darwin_options = [
                '-Dcocoa=on',
                '-Dbonjour=on',
                '-Dcastor=OFF',
                '-Drfio=OFF',
                '-Ddcache=OFF']
            options.extend(darwin_options)
        with working_dir(build_directory, create=True):
            cmake(*options)
            make()
            make("install")

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
