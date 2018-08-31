from spack import *
import os

class Thepeg(Package):

    url      = "http://www.hepforge.org/archive/thepeg/ThePEG-2.1.4.tar.bz2"

    version('2.1.4', sha256='400c37319aa967ed993fdbec84fc65b24f6cb3779fb1b173d7f5d7a56b772df5')

    patch('thepeg-2.1.1-gcc8.patch')

    depends_on('lhapdf')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('zlib')
    depends_on('rivet')
    depends_on('fastjet')

    def install(self,spec,prefix):
        autoreconf('-fiv')
        configure('--prefix=%s' % prefix,
                '--enable-shared',
                '--disable-static',
                '--with-lhapdf=%s'%spec['lhapdf'].prefix,
                '--with-boost=%s'%spec['boost'].prefix,
                '--with-hepmc=%s'%spec['hepmc'].prefix,
                '--with-gsl=%s'%spec['gsl'].prefix,
                '--with-zlib=%s'%spec['zlib'].prefix,
                '--with-fastjet=%s'%spec['fastjet'].prefix,
                '--with-rivet=%s'%spec['rivet'].prefix,
                '--without-javagui',
                '--disable-readline')
        make('VERBOSE=1','install')
        with working_dir('%s/ThePEG'%prefix.lib):
            os.symlink('LesHouches.so','libLesHouches.so')
