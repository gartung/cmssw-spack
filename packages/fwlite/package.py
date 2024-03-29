from spack import *
from glob import glob
from string import Template
import re
import os
import fnmatch
import sys
import shutil


class Fwlite(CMakePackage):
    """CMSSW FWLite built with cmake"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/gartung/fwlite/archive/refs/tags/11.3.1.2.tar.gz"

    version('master', git='https://github.com/gartung/fwlite.git',tag='master')
    version('11.3.1.2', sha256='0b293f6ad704faea3cc9e046542f1f86c9245ab30d39a2b54ba4d7423e6acfe6')

    resource(name='cmaketools', git='https://github.com/gartung/cmaketools.git',
              placement='cmaketools')
    resource(name='upgrade-geometry', url='http://cmsrep.cern.ch/cmssw/download/Fireworks-Geometry/20200401/cmsGeom2026.root',
              placement='data', sha256='3077e4d9abd62c57d1d71b30fa968ba52a7c12879a7fc71d90d94c4123e426fa', expand=False)
    resource(name='geometry', url='https://github.com/cms-data/Fireworks-Geometry/archive/V07-06-00.tar.gz',
              placement='data/Fireworks/Geometry/data', sha256='93312e7c60525c66c09c86fdc36db401c281b95ccb2d9195d735f84506f5868b')
    resource(name='patcandidates', url='https://github.com/cms-data/DataFormats-PatCandidates/archive/V01-00-01.tar.gz',
              placement='data/DataFormats/PatCandidates/data', sha256='5a0941df5a191d0f942e26838103659970ba29cb9cd4ab3d0cc45bcc01b408df')
    resource(name='miniaod', url='https://cmsshow-rels.web.cern.ch/cmsShow-rels/samples/11_2/RelValZTTminiaod.root',
              placement='data/samples/11_2/miniaod', sha256='4c4ddc418c7131f6eea16ea4bfefa36c2dba8ac2161640bf93b1d7889ce8fa2c', expand=False)
    resource(name='aod', url='https://cmsshow-rels.web.cern.ch/cmsShow-rels/samples/11_2/RelVallZTTGenSimReco.root',
              placement='data/samples/11_2/aod', sha256='209e6bda0496892d33137bf67ecb583b233e4c962154b6ca574aa33f824ea532', expand=False)

    if sys.platform != 'darwin':
        patch('patch')
    if sys.platform == 'darwin':
        depends_on('libuuid')
    depends_on('cmake', type='build')
    depends_on('root+aqua+opengl~x~tbb')
    depends_on('intel-tbb-oneapi')
    depends_on('clhep')
    depends_on('md5-cms')
    depends_on('python')
    depends_on('vdt')
    depends_on('boost')
    depends_on('py-pybind11', type=('link', 'run', 'test'))
    depends_on('hepmc')
    depends_on('pcre')
    depends_on('davix')
    depends_on('libsigcpp@2.10.3')
    depends_on('tinyxml2@6.2.0')
    depends_on('jpeg')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('fmt')
    depends_on('eigen')
    depends_on('openssl')

    def cmake_args(self):
        cxxstd = self.spec['root'].variants['cxxstd'].value
        args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path,
                '-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix,
                '-DBOOST_ROOT=%s' % self.spec['boost'].prefix,
                '-DTBB_ROOT_DIR=%s' % self.spec['intel-tbb-oneapi'].prefix,
                '-DCMSMD5ROOT=%s' % self.spec['md5-cms'].prefix,
                '-DDAVIXROOT=%s' % self.spec['davix'].prefix,
                '-DSIGCPPROOT=%s' % self.spec['libsigcpp'].prefix,
                '-DSIGCPP_INCLUDE_DIR=%s/sigc++-2.0' % self.spec['libsigcpp'].prefix.include,
                '-DSIGCPP_LIB_INCLUDE_DIR=%s/sigc++-2.0/include' % self.spec['libsigcpp'].prefix.lib,
                '-DTINYXML2ROOT=%s' % self.spec['tinyxml2'].prefix,
                '-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix,
                '-DXERCESC_ROOT_DIR=%s' % self.spec['xerces-c'].prefix]
        args.append('-DFMT_INCLUDE_DIR=%s' % self.spec['fmt'].prefix.include)
        args.append('-DOPENSSL_INCLUDE_DIR=%s' % self.spec['openssl'].prefix.include)
        args.append('-DEIGEN_INCLUDE_DIR=%s' % self.spec['eigen'].prefix.include)
        args.append('-DVDT_ROOT_DIR=%s' % self.spec['vdt'].prefix)
        args.append('-DCMAKE_CXX_STANDARD=%s' % cxxstd)
        if sys.platform == 'darwin':
            args.append('-DUUID_INCLUDE_DIR=%s/include' %
                           self.spec['libuuid'].prefix)
            args.append('-DUUID_ROOT_DIR=%s' %
                           self.spec['libuuid'].prefix)
        return(args)

    @run_before('cmake')
    def move_data(self):
        cmssw_version = 'CMSSW.' + str(self.version[:-1])
        cmssw_u_version = cmssw_version.replace('.', '_')
        mkdirp(join_path(self.stage.source_path,'Fireworks/Core/data'))
        with open(join_path(self.stage.source_path,'Fireworks/Core/data/version.txt'), 'w') as f:
            f.write('%s' % cmssw_u_version)
        shutil.move(join_path(self.stage.source_path, 'data', 'cmsGeom2026.root'), join_path(self.stage.source_path, 'data/Fireworks/Geometry/data', 'cmsGeom2026.root'))

    @run_before('install')
    def install_data(self):
        install_tree(join_path(self.stage.source_path,'data'), join_path(self.prefix,'data'))

    def setup_run_environment(self, env):
        cmssw_version = 'CMSSW.' + str(self.version[:-1])
        cmssw_u_version = cmssw_version.replace('.', '_')
        env.set('CMSSW_VERSION', cmssw_u_version)
        env.set('ROOT_INCLUDE_PATH', self.prefix.src)
        env.set('CMSSW_RELEASE_BASE', self.prefix)
        env.set('CMSSW_BASE', '%s' % self.prefix)
        env.set('CMSSW_DATA_PATH', '%s/data' % self.prefix)
        env.set('CMSSW_SEARCH_PATH', '%s/data/Fireworks/Geometry/data' % self.prefix)
        if sys.platform == 'darwin':
            env.set('DYLD_FALLBACK_LIBRARY_PATH', self.prefix.lib)
        else: 
            env.set('LD_LIBRARY_PATH', self.prefix.lib)
