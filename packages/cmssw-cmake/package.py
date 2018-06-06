from spack import *
from glob import glob
from string import Template
import re
import os
import fnmatch
import sys
import shutil


class CmsswCmake(Package):
    """CMSSW built with Cmakefile generated by scram2cmake"""

    homepage = "http://cms-sw.github.io"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc_amd64_gcc630/cms/cmssw/CMSSW_9_2_12/src.tar.gz"

    version('10.2.0.pre1', git='https://github.com/cms-sw/cmssw.git',
            tag='CMSSW_10_2_0_pre1')

    resource(name='cmaketools', git='https://github.com/gartung/cmaketools.git',
             commit='df41c9ce7c950397ed52b289887144749b866b24',
             placement='cmaketools'
             )

    resource(name='scram2cmake', git='https://github.com/gartung/scram2cmake.git',
             commit='034c581',
             placement='scram2cmake'
             )

    depends_on('builtin.ninja')
    depends_on('builtin.cmake')
    depends_on('root')
    depends_on('intel-tbb')
    depends_on('tinyxml')
    depends_on('clhep~cxx11+cxx14')
    depends_on('md5')
    depends_on('python+shared')
    depends_on('vdt')
    depends_on('boost@1.63.0')
    depends_on('libsigcpp')
    depends_on('xrootd')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite')
    depends_on('bzip2')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('heppdt')
    depends_on('libpng')
    depends_on('giflib')
    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('xz')
    depends_on('libtiff')
    depends_on('libjpeg-turbo')
    depends_on('libxml2')
    depends_on('bzip2')
    depends_on('fireworks-geometry')
    depends_on('llvm')
    depends_on('uuid-cms')
    depends_on('valgrind')
    depends_on('geant4')
    depends_on('expat')
    depends_on('protobuf')
    depends_on('eigen')
    depends_on('curl')
    depends_on('classlib')
    depends_on('davix')
    depends_on('meschach')
    depends_on('fastjet')
    depends_on('fastjet-contrib')
    depends_on('fftjet')
    depends_on('pythia6')
    depends_on('pythia8')
    depends_on('occi')
    depends_on('oracle')
    depends_on('sqlite')
    depends_on('coral')
    depends_on('hector')
    depends_on('geant4-g4emlow')
    depends_on('geant4-g4ndl')
    depends_on('geant4-g4photonevaporation')
    depends_on('geant4-g4saiddata')
    depends_on('geant4-g4abla')
    depends_on('geant4-g4ensdfstate')
    depends_on('geant4-g4neutronsxs')
    depends_on('geant4-g4radioactivedecay')
    depends_on('libhepml')
    depends_on('lhapdf')
    depends_on('utm')
    depends_on('photospp')
    depends_on('rivet')
    depends_on('evtgen')
    depends_on('dcap')
    depends_on('tauolapp')
    depends_on('sherpa')
    depends_on('lwtnn')
    depends_on('yoda')
    depends_on('openloops')
    depends_on('qd')
    depends_on('blackhat')
    depends_on('yaml-cpp')
    depends_on('jemalloc')
    depends_on('ktjet')
    depends_on('herwig')
    depends_on('photos')
    depends_on('tauola')
    depends_on('jimmy')
    depends_on('cascade')
    depends_on('csctrackfinderemulation')
    depends_on('mcdb')
    depends_on('fftw') 
    depends_on('netlib-lapack')
    depends_on('tensorflow')
    depends_on('dd4hep')
 
    def install(self, spec, prefix):
        s2c=Executable('scram2cmake/scram2cmake.py')
        s2c()
        with working_dir('spack-build', create=True):
            options = ['../']
            options.extend(std_cmake_args)
            for d in self.spec.traverse(root=False, deptype=('link')):
                var = '%s_INCLUDE_DIR' % d.name.upper()
                opt = '-D%s=%s' % (var, str(self.spec[d.name].prefix.include))
                options.append(opt)
            if sys.platform == 'darwin':
                options.append('-DUUID_INCLUDE_DIR=%s/include' %
                               self.spec['libuuid'].prefix)
                options.append('-DUUID_ROOT_DIR=%s' %
                               self.spec['libuuid'].prefix)
            args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path,
                    '-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix,
                    '-DBOOST_ROOT=%s' % self.spec['boost'].prefix,
                    '-DTBB_ROOT_DIR=%s' % self.spec['intel-tbb'].prefix,
                    '-DMD5ROOT=%s' % self.spec['md5'].prefix,
                    '-DDAVIXROOT=%s' % self.spec['davix'].prefix,
                    '-DSIGCPPROOT=%s' % self.spec['libsigcpp'].prefix,
                    '-DSIGCPP_INCLUDE_DIR=%s/sigc++-2.0' % self.spec['libsigcpp'].prefix.include,
                    '-DSHERPA_INCLUDE_DIR=%s/SHERPA-MC' % self.spec['sherpa'].prefix.include,
                    '-DDAVIX_INCLUDE_DIR=%s/davix' % self.spec['davix'].prefix.include,
                    '-DXROOTD_INCLUDE_DIR=%s/xrootd' % self.spec['xrootd'].prefix.include,
                    '-DTINYXMLROOT=%s' % self.spec['tinyxml'].prefix,
                    '-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix,
                    '-DXERCESC_ROOT_DIR=%s' % self.spec['xerces-c'].prefix,
                    '-DGEANT4_INCLUDE_DIRS=%s/Geant4' % self.spec['geant4'].prefix.include,
                    '-DGEANT4_DIR=%s' % self.spec['geant4'].prefix,
                    '-DPYTHON_INCLUDE_DIR=%s/python%s' % (self.spec['python'].prefix.include, self.spec['python'].version.up_to(2)),
                    '-DCMAKE_CXX_FLAGS=-O2 -pthread -pipe -Werror=main -Werror=pointer-arith -Werror=overlength-strings -Wno-vla -Werror=overflow   -std=c++1z -ftree-vectorize -Wstrict-overflow -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits -fvisibility-inlines-hidden -fno-math-errno --param vect-max-version-for-alias-checks=50 -Xassembler --compress-debug-sections -msse3 -felide-constructors -fmessage-length=0 -Wall -Wno-non-template-friend -Wno-long-long -Wreturn-type -Wunused -Wparentheses -Wno-deprecated  -Wnon-virtual-dtor -fdiagnostics-show-option -Wno-unused-local-typedefs -Wno-attributes'
                    ,'-GNinja']
#                    ,]
            options.extend(args)
            cmake(*options)
#            make('-k','VERBOSE=1')
#            make('install')
            ninja('-k','-1', '-v')
            ninja('install')

