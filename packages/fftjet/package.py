from spack import *
import sys,os


class Fftjet(AutotoolsPackage):

    url = "https://www.hepforge.org/archive/fftjet/fftjet-1.5.0.tar.gz"

    version('1.5.0', '9f91b6974c00ba546833c38d5b3aa563')

    depends_on('fftw')

    def configure_args(self):
        args = ['--disable-dependency-tracking',
                '--enable-threads',
                'CFLAGS=-fpic',
                'DEPS_CFLAGS=-I%s' % self.spec['fftw'].prefix.include,
                'DEPS_LIBS="-L%s -lfftw3"' % self.spec['fftw'].prefix.lib]
        return args
