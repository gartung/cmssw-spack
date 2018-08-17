from spack import *
import glob
import sys,os



class Hector(Package):
    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/hector/1.3.4_patch1-fmblme3/hector-1.3.4_patch1.tgz"
    depends_on('root')

    version('1.3.4_patch1', '419ec3ce8dfbcff972ea6d5b09e8c6f1')

    def install(self, spec, prefix):
        mkdirp('obj')
        mkdirp('lib')
        make()
        cp = which('cp')
        for f in glob.glob('*'):
            cp('-r', f, prefix)
