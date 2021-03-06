from spack import *
from glob import glob
from string import Template
import re
import os
import fnmatch
import sys


class FwliteCmake(Package):
    """CMSSW FWLite built with cmake"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/cms-sw/cmssw/archive/CMSSW_9_0_0.tar.gz"

    version('9.0.1', git='https://github.com/gartung/fwlite.git',
            commit='6a9ace6', submodules=True)
    version('9.2.6', git='https://github.com/gartung/fwlite.git',
            commit='70f937c', submodules=True)

    if sys.platform != 'darwin':
        patch('patch')
    if sys.platform == 'darwin':
        depends_on('cfe-bindings')
        depends_on('libuuid')
    depends_on('cmake', type='build')
    depends_on('ninja', type='build')
    depends_on('root')
    depends_on('tbb')
    depends_on('clhep')
    depends_on('md5')
    depends_on('python')
    depends_on('vdt')
    depends_on('boost+python')
    depends_on('xrootd')
    depends_on('hepmc')
    depends_on('pcre')
    depends_on('davix')
    depends_on('libsigcpp')
    depends_on('tinyxml')
    depends_on('jpeg')
    depends_on('cppunit')
    depends_on('fireworks-data')
    depends_on('xerces-c')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            options = ['../']
            options.extend(std_cmake_args)
            args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path,
                    '-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix,
                    '-DBOOST_ROOT=%s' % self.spec['boost'].prefix,
                    '-DTBB_ROOT_DIR=%s' % self.spec['tbb'].prefix,
                    '-DMD5ROOT=%s' % self.spec['md5'].prefix,
                    '-DDAVIXROOT=%s' % self.spec['davix'].prefix,
                    '-DSIGCPPROOT=%s' % self.spec['libsigcpp'].prefix,
                    '-DSIGCPP_INCLUDE_DIR=%s/include/sigc++-2.0' % self.spec['libsigcpp'].prefix,
                    '-DTINYXMLROOT=%s' % self.spec['tinyxml'].prefix,
                    '-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix,
                    '-DXERCESC_ROOT_DIR=%s' % self.spec['xerces-c'].prefix]
            options.extend(args)
            if sys.platform == 'darwin':
                options.append('-DUUID_INCLUDE_DIR=%s/include' %
                               self.spec['libuuid'].prefix)
                options.append('-DUUID_ROOT_DIR=%s' %
                               self.spec['libuuid'].prefix)
            options.append('-GNinja')
            cmake(*options)
            ninja = which('ninja')
            ninja('-v', '-j4')
            ninja('install')
