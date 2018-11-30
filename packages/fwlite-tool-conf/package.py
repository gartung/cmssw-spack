from spack import *
import re
import os, sys
from glob import glob
import fnmatch


class FwliteToolConf(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('scram')
    depends_on('gmake-toolfile')
    if sys.platform == 'darwin':
        depends_on('cfe-bindings')
    else:
        depends_on('llvm-lib-toolfile')
    depends_on('gcc-compiler-toolfile')
    depends_on('root-toolfile')
    depends_on('intel-tbb-toolfile')
    depends_on('tinyxml-toolfile')
    depends_on('tinyxml2-toolfile')
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
    depends_on('uuid-toolfile')

    def install(self, spec, prefix):
        with working_dir(prefix, create=True):
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep in spec.dependencies():
                xmlfiles = glob(join_path(dep.prefix.etc, 'scram.d', '*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile, 'tools/selected')
