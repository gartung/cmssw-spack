from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Tauolapp(Package):
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-1.1.5-src.tgz"


    version('1.1.5', '2d9a3bc7536ddc5d937bbe711ddbadbe')


    depends_on('hepmc')
    depends_on('pythia8')
    depends_on('lhapdf')
    depends_on('boost')

    def patch(self):
        with working_dir(str(self.version)):
            if os.path.exists('./config/config.sub'):
                os.remove('./config/config.sub')
                install(join_path(os.path.dirname(__file__), '../../config.sub'), './config/config.sub')
            if os.path.exists('./config/config.guess'):
                os.remove('./config/config.guess')
                install(join_path(os.path.dirname(__file__), '../../config.guess'), './config/config.guess')


    def setup_environment(self, spack_env, run_env):
        self.HEPMC_ROOT = self.spec['hepmc'].prefix
        self.HEPMC_VERSION = self.spec['hepmc'].version
        self.LHAPDF_ROOT = self.spec['lhapdf'].prefix
        self.PYTHIA8_ROOT = self.spec['pythia8'].prefix
        spack_env.set('HEPMCLOCATION',self.HEPMC_ROOT)
        spack_env.set('HEPMCVERSION',self.HEPMC_VERSION)
        spack_env.set('LHAPDF_LOCATION',self.LHAPDF_ROOT)
        spack_env.set('PYTHIA8_LOCATION',self.PYTHIA8_ROOT)


    def install(self, spec, prefix):
        with working_dir(str(self.version)):
            configure('--prefix=%s' % prefix,
                      '--with-hepmc=%s' % self.HEPMC_ROOT,
                      '--with-pythia8=%s' % self.PYTHIA8_ROOT,
                      '--with-lhapdf=%s' % self.LHAPDF_ROOT,
                      'CPPFLAGS=-I%s/include' % self.spec['boost'].prefix)
            make()
            make('install')
            mkdirp(prefix.share)
            with working_dir(join_path(self.stage.source_path, str(self.version), 
                    'TauSpinner/examples/CP-tests/Z-pi')):
                for f in glob.glob('*.txt'):    
                    install(f, join_path(prefix.share, f))
