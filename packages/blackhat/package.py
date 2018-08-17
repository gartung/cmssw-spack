from spack import *
import sys,os

class Blackhat(Package):

    url      = "http://www.hepforge.org/archive/blackhat/blackhat-0.9.9.tar.gz"

    version('0.9.9', '64a4e64a95754bb701bf0c1f88c8ee53')

    patch('blackhat-gcc48.patch')
#    patch('blackhat-0.9.9-armv7hl.patch')
    patch('blackhat-no_warnings.patch')
    patch('blackhat-0.9.9-default-arg-at-first-decl.patch')
    patch('blackhat-0.9.9-gcc600.patch')



    depends_on('qd')
    depends_on('openssl')
    depends_on('python')

    def patch(self):
        if os.path.exists('./config/config.sub'):
            os.remove('./config/config.sub')
            install(join_path(os.path.dirname(__file__), '../../config.sub'), './config/config.sub')
        if os.path.exists('./config/config.guess'):
            os.remove('./config/config.guess')
            install(join_path(os.path.dirname(__file__), '../../config.guess'), './config/config.guess')



    def install(self, spec, prefix):
        QD_ROOT=spec['qd'].prefix
        OPENSSL_ROOT=spec['openssl'].prefix
        configure('--prefix=%s' % prefix,
                '--with-QDpath=%s' % QD_ROOT,
                'CXXFLAGS=-Wno-deprecated -I%s/include' % OPENSSL_ROOT,
                'LDFLAGS=-L%s/lib' % OPENSSL_ROOT)
        make()
        make('install')

