from spack import *


class Gosamcontrib(AutotoolsPackage):

    homepage = "http://www.example.com"
    url      = "http://www.hepforge.org/archive/gosam/gosam-contrib-2.0-20150803.tar.gz"

    version('2.0-20150803', sha256='d8fcbfe4270ce250f37366e39b5cd19528bd520658930b3d204df29b905314da')

    depends_on('qgraf')
    depends_on('form')


    def setup_environment(self, spack_env, run_env):
        spack_env.set('CXX',spack_cxx+' -fpic')
        spack_env.set('CC',spack_cc+' -fpic')
        spack_env.set('F77',spack_f77+' -std=legacy')
        spack_env.set('FC',spack_fc+' -std=legacy')

    def configure_args(self):
        args = ['--enable-shared', '--enable-static']
        return args
