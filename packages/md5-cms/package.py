from spack import *
import sys,os

class Md5Cms(Package):
    url = 'https://github.com/cms-externals/md5.git'

    version('1.0.0', git='https://github.com/cms-externals/md5.git',
                branch='cms/1.0.0')

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
        cp('-v', 'md5.h', '%s/md5-cms.h' % prefix.include)
