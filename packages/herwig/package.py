from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Herwig(Package):
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/herwig/herwig-6.521-src.tgz"

    version('6.521.2', 'f5eebb2d2318dc437ec534eb430293d9')
    version('6.521',   '61bfc32cbf25fe92e9e3e7f23be1338f')


    depends_on('lhapdf')
    depends_on('photos')

    def install(self, spec, prefix):
        with working_dir(self.version.string):
            configure('--enable-static', '--disable-shared', '--prefix=%s' % prefix, 'F77=gfortran -fPIC')
            make('LHAPDF_ROOT=%s' % spec['lhapdf'],
                 'PHOTOS_ROOT=%s' % spec['photos'])
            make('check')
            make('install')
        os.symlink('%s/HERWIG65.INC' % prefix.include, '%s/herwig65.inc'% prefix.include)

