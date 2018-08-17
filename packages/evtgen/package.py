from spack import *
import glob
import shutil
import sys,os


class Evtgen(Package):

    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/evtgen/evtgen-1.6.0-src.tgz"

    version('1.6.0', '6f81a213c03ed41f9a7f2e6225e42330')
    version('1.5.0', 'e979afdf58858a3f2f760594304cd9f3')

    depends_on('hepmc')
    depends_on('pythia8')
    depends_on('tauolapp')
    depends_on('photospp')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')

    patch('evtgen-1.6.0-configure-new-gcc.patch')


    def install(self, spec, prefix):
        with working_dir(str(self.version)):
            args = ['--prefix=%s' % prefix,
                    '--hepmcdir=%s' % self.spec['hepmc'].prefix,
                    '--pythiadir=%s' % self.spec['pythia8'].prefix,
                    '--tauoladir=%s' % self.spec['tauolapp'].prefix,
                    '--photosdir=%s' % self.spec['photospp'].prefix
                    ]
            configure(*args)
            make('-j1', 'VERBOSE=1')
            make('install')
        for f in glob.glob(prefix.lib+'/archive/*.a'):
            shutil.move(f, '../'+os.path.basename(f))
        shutil.rmtree(prefix.lib+'/archive')

