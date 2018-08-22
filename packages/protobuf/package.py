from spack import *
import spack.util.web
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Protobuf(AutotoolsPackage):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url = "https://github.com/google/protobuf/archive/v3.2.0.tar.gz"
    root_cmakelists_dir = "cmake"

    version('3.5.2', 'ff6742018c172c66ecc627029ad54280')
    version('3.4.0', '1d077a7d4db3d75681f5c333f2de9b1a')
    version('3.3.0', 'f0f712e98de3db0c65c0c417f5e7aca8')
    version('3.2.0', 'efaa08ae635664fb5e7f31421a41a995')
    version('3.1.0', '39d6a4fa549c0cce164aa3064b1492dc')
    version('3.0.2', '7349a7f43433d72c6d805c6ca22b7eeb')
    # does not build with CMake:
    # version('2.5.0', '9c21577a03adc1879aba5b52d06e25cf')

    depends_on('zlib')
    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build') 
    depends_on('libtool', type='build')

    conflicts('%gcc@:4.6')  # Requires c++11


    def configure_args(self):
        args = [
            '--disable-static',
            '--disable-dependency-tracking',
            'CXXFLAGS=-I%s' % self.spec['zlib'].prefix.include,
            'CFLAGS=-I%s' % self.spec['zlib'].prefix.include,
            'LDFLAGS=-L%s' % self.spec['zlib'].prefix.lib
        ]
        return args

    def setup_dependent_environment(self,spack_env,run_env,dspec):
        spack_env.set('PROTOBUF_SOURCE','https://github.com/google/protobuf/archive/v%s.tar.gz'%self.version)
        spack_env.set('PROTOBUF_STRIP_PREFIX','protobuf-%s'%self.version)

