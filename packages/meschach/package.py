from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Meschach(Package):
    homepage = "http://www.example.com"
    url = "http://homepage.divms.uiowa.edu/~dstewart/meschach/mesch12b.tar.gz"

    version('12b', '4ccd520f30934ebc34796d80dab29e5c')

    patch('meschach-1.2b-fPIC.patch', level=0)
    patch('meschach-1.2-slc4.patch')

    def install(self, spec, prefix):
        make('all')
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        for f in glob.glob('*.h'):
            install(f, prefix.include + '/' + f)
        install('meschach.a', prefix.lib + '/libmeschach.a')

