from spack import *
import re
import os
from glob import glob
from string import Template
import fnmatch


class CoralToolConf(Package):

    url='file://'

    version('1.0', '', expand=False)

    depends_on('scram') # provides gcc-toolfile systemtools
    depends_on('gmake-toolfile')
    depends_on('pcre-toolfile')
    depends_on('python-toolfile')
    depends_on('expat-toolfile')
    depends_on('boost-toolfile')
    depends_on('frontier-client-toolfile')
    depends_on('openssl-toolfile')


    depends_on('sqlite-toolfile')
    depends_on('uuid-cms-toolfile')
    depends_on('zlib-toolfile')
    depends_on('bzip2-toolfile')
    depends_on('cppunit-toolfile')
    depends_on('xerces-c-toolfile')
    depends_on('oracle-toolfile')


    def install(self, spec, prefix):

        install_tree(self.stage.source_path,prefix+'/tools')
