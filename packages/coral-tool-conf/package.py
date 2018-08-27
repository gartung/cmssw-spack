from spack import *
import re
import os
from glob import glob
import fnmatch


class CoralToolConf(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('scram') # provides gcc-toolfile systemtools
    depends_on('gmake-toolfile')
    depends_on('pcre-toolfile')
    depends_on('python-toolfile')
    depends_on('expat-toolfile')
    depends_on('boost-toolfile')
    depends_on('frontier-client-toolfile')
    depends_on('openssl-toolfile')


    depends_on('sqlite-toolfile')
    depends_on('uuid-toolfile')
    depends_on('zlib-toolfile')
    depends_on('bzip2-toolfile')
    depends_on('cppunit-toolfile')
    depends_on('xerces-c-toolfile')
    depends_on('oracle-toolfile')
    depends_on('cms-oracleocci-abi-hack-toolfile')


    def install(self, spec, prefix):
        with working_dir(prefix, create=True):
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep in spec.dependencies():
                xmlfiles = glob(join_path(dep.prefix.etc, 'scram.d', '*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile, 'tools/selected')
