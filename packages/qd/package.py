from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Qd(Package):
    homepage = "http://www.example.com"
    url      = "http://crd.lbl.gov/~dhbailey/mpdist/qd-2.3.13.tar.gz"
    
    version('2.3.18', '48e788826c0c610f4f0eb49e5465a32b')


    def patch(self):
        os.remove('./config/config.sub')
        os.remove('./config/config.guess')
        install(join_path(os.path.dirname(__file__), '../../config.sub'), './config/config.sub')
        install(join_path(os.path.dirname(__file__), '../../config.guess'), './config/config.guess')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--enable-shared')
        make()
        make('install')
