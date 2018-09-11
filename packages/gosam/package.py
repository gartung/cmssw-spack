from spack import *


class Gosam(Package):
    url      = "http://www.hepforge.org/archive/gosam/gosam-2.0.4-33b41ed.tar.gz"

    version('2.0.4-33b41ed', sha256='1f969a4620391c084fb2061fa4bcac5807757f2259b40b13fce17ffd32b53857',
            url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/gosam/2.0.4-33b41ed/gosam-2.0.4-33b41ed.tar.gz')

    depends_on('qgraf')
    depends_on('form')
    depends_on('gosamcontrib')
    depends_on('python')
    depends_on('py-cython')

    def install(self, spec, prefix):
        python=which('python')
        python('setup.py', 'install', '--prefix=%s'%prefix)
