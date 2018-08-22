from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Mcdb(Package):
    homepage = "http://www.example.com"
    url = "http://mcdb.cern.ch/distribution/api/mcdb-api-1.0.3.tar.gz"

    version('1.0.3', '587a2699d3240561ccaf479c8edcfdeb')
    version('1.0.2', 'f8c5cba0b66c7241115bc74e846c7814')
    version('1.0.1', 'c93bafcfc129a875ce5097c4e5fcf16e')


    depends_on('xerces-c')

    def install(self, spec, prefix):
        contents = """
PLATFORM = slc_amd64_gcc
CC       = gcc
CXX      = g++
CFLAGS   = -O2 -pipe -Wall -W -fPIC
CXXFLAGS = -O2 -pipe -Wall -W -fPIC
LINK     = g++
LFLAGS   = -shared -Wl,-soname,libmcdb.so
XERCESC  = %s
""" % spec['xerces-c'].prefix

        make()
        install_tree('lib', prefix + '/lib')
        install_tree('interface', prefix + '/interface')

