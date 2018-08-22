from spack import *
import sys
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Md5(Package):
    url = "http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/md5/1.0.0-giojec/md5.1.0.0-d97a571864a119cd5408d2670d095b4410e926cc.tgz"

    version('1.0.0', 'b154f78e89a70ac1328099d9c3820d13',
            url='http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/md5/1.0.0-giojec/md5.1.0.0-d97a571864a119cd5408d2670d095b4410e926cc.tgz')

    def install(self, spec, prefix):
        comp = which('gcc')
        cp = which('cp')
        md = which('mkdir')
        md('%s' % prefix.lib)
        md('%s' % prefix.include)
        if sys.platform == 'darwin':
            comp('md5.c', '-shared', '-fPIC', '-o', 'libcms-md5.dylib')
            cp('-v', 'libcms-md5.dylib', prefix.lib)
            fix_darwin_install_name(prefix.lib)
        else:
            comp('md5.c', '-shared', '-fPIC', '-o', 'libcms-md5.so')
            cp('-v', 'libcms-md5.so', prefix.lib)
        cp('-v', 'md5.h', prefix.include)
