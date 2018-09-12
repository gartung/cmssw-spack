from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Lwtnn(CMakePackage):
    homepage = "http://www.example.com"
    url      = "https://github.com/lwtnn/lwtnn/archive/v1.0.tar.gz"

    version('2.4', 'e323debb51fdd251e7f74238f757a952')
    version('1.0', 'bb62cd8c1f0a97681206894f7f5a8e95')

    depends_on('boost')
    depends_on('eigen')
    depends_on('cmake', type='build')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('BOOST_ROOT', self.spec['boost'].prefix)
        spack_env.set('EIGEN_ROOT', self.spec['eigen'].prefix)

    def cmake_args(self):
        args= (
             '-DCMAKE_CXX_COMPILER=g++',
             '-DCMAKE_CXX_FLAGS=-fPIC',
             '-DCMAKE_BUILD_TYPE=Release',
             '-DBUILTIN_BOOST=OFF',
             '-DBUILTIN_EIGEN=OFF')
        return args
