from spack import *
import re
import os
from glob import glob
import fnmatch


class CmsswToolConf(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('scram')
    depends_on('gmake-toolfile')
    depends_on('root-toolfile')
    depends_on('intel-tbb-toolfile')
    depends_on('tinyxml-toolfile')
    depends_on('clhep-toolfile')
    depends_on('md5-toolfile')
    depends_on('python-toolfile')
    depends_on('vdt-toolfile')
    depends_on('boost-toolfile')
    depends_on('libsigcpp-toolfile')
    depends_on('xrootd-toolfile')
    depends_on('cppunit-toolfile')
    depends_on('xerces-c-toolfile')
    depends_on('expat-toolfile')
    depends_on('sqlite-toolfile')
    depends_on('bzip2-toolfile')
    depends_on('gsl-toolfile')
    depends_on('hepmc-toolfile')
    depends_on('heppdt-toolfile')
    depends_on('libpng-toolfile')
    depends_on('giflib-toolfile')
    depends_on('openssl-toolfile')
    depends_on('pcre-toolfile')
    depends_on('zlib-toolfile')
    depends_on('xz-toolfile')
    depends_on('libtiff-toolfile')
    depends_on('libjpeg-turbo-toolfile')
    depends_on('libxml2-toolfile')
    depends_on('bzip2-toolfile')
    depends_on('fireworks-geometry-toolfile')
    depends_on('llvm-lib-toolfile')
    depends_on('uuid-toolfile')
    depends_on('dd4hep-toolfile')
    depends_on('geant4-toolfile')
    depends_on('expat-toolfile')
    depends_on('protobuf-toolfile')
    depends_on('eigen-toolfile')
    depends_on('curl-toolfile')
    depends_on('classlib-toolfile')
    depends_on('davix-toolfile')
    depends_on('meschach-toolfile')
    depends_on('fastjet-toolfile')
    depends_on('fastjet-contrib-toolfile')
    depends_on('fftjet-toolfile')
    depends_on('pythia6-toolfile')
    depends_on('pythia8-toolfile')
    depends_on('oracle-toolfile')
    depends_on('cms-oracleocci-abi-hack-toolfile')
    depends_on('sqlite-toolfile')
    depends_on('coral-toolfile')
    depends_on('hector-toolfile')
    depends_on('geant4-g4emlow-toolfile')
    depends_on('geant4-g4ndl-toolfile')
    depends_on('geant4-g4photonevaporation-toolfile')
    depends_on('geant4-g4saiddata-toolfile')
    depends_on('geant4-g4abla-toolfile')
    depends_on('geant4-g4ensdfstate-toolfile')
    depends_on('geant4-g4neutronsxs-toolfile')
    depends_on('geant4-g4radioactivedecay-toolfile')
    depends_on('libhepml-toolfile')
    depends_on('lhapdf-toolfile')
    depends_on('utm-toolfile')
    depends_on('photospp-toolfile')
    depends_on('rivet-toolfile')
    depends_on('evtgen-toolfile')
    depends_on('dcap-toolfile')
    depends_on('tauolapp-toolfile')
    depends_on('sherpa-toolfile')
    depends_on('lwtnn-toolfile')
    depends_on('yoda-toolfile')
    depends_on('openloops-toolfile')
    depends_on('qd-toolfile') 
    depends_on('blackhat-toolfile')
    depends_on('yaml-cpp-toolfile')
    depends_on('jemalloc-toolfile')
    depends_on('ktjet-toolfile')
    depends_on('herwig-toolfile')
    depends_on('photos-toolfile')
    depends_on('tauola-toolfile')
    depends_on('jimmy-toolfile')
    depends_on('cascade-toolfile')
    depends_on('csctrackfinderemulation-toolfile')
    depends_on('mcdb-toolfile')
    depends_on('fftw-toolfile')
    depends_on('netlib-lapack-toolfile')
    depends_on('frontier-client-toolfile')
    depends_on('tkonlinesw-toolfile')
    depends_on('valgrind-toolfile')

    def install(self, spec, prefix):
        with working_dir(prefix, create=True):
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep in spec.dependencies():
                xmlfiles = glob(join_path(dep.prefix.etc, 'scram.d', '*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile, 'tools/selected')
