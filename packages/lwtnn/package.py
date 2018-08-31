from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Lwtnn(Package):
    homepage = "http://www.example.com"
    url      = "https://github.com/lwtnn/lwtnn/archive/v1.0.tar.gz"

    version('1.0', 'bb62cd8c1f0a97681206894f7f5a8e95')

    depends_on('boost')
    depends_on('eigen')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('BOOST_ROOT', self.spec['boost'].prefix)
        spack_env.set('EIGEN_ROOT', self.spec['eigen'].prefix)

    def install(self, spec, prefix):
        make('all')
        install_tree('lib', self.prefix.lib)
        install_tree('bin', self.prefix.bin)
        install_tree('include', self.prefix.include)
