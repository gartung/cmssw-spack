from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Dd4hep(CMakePackage):
    """software framework of the FCC project"""
    homepage = "https://github.com/AIDASoft/DD4hep/"
    url      = "https://github.com/AIDASoft/DD4hep/archive/v01-02.tar.gz"

    version('01.07', git='https://github.com/cms-externals/DD4hep.git',
             commit='ffe3645730224bf0b0a6dd6a8d2c6c1d87fa2b53')
    version('01.05', 'ab9aaa59e9d9ad9d60205151d984ec2b')
    version('01.02', 'bcef07aaf7a28b5ed9062a76a7ba5633')
    version('00.19', 'f5e162261433082c6363e6c96c08c66e')
    version('00.18', 'ab4f3033c9ac7494f863bc88eedbdcf5')
    version('00.17', '9b9ea29790aa887893484ed8a4afae68')
    version('00.16', '4df618f2f7b10f0e995d7f30214f0850')
    version('00.15', 'cf0b50903e37c30f2361318c79f115ce')

    depends_on('cmake', type='build')
    depends_on('boost')
    depends_on('xerces-c')
    depends_on('root')
    depends_on('clhep')

    def cmake_args(self):
        spec = self.spec

        options = []

        # Set the correct compiler flag
        #if self.compiler.cxx11_flag:
        #    options.extend(['-DDD4HEP_USE_CXX11=ON'])
        #if self.compiler.cxx14_flag:
        #    options.extend(['-DDD4HEP_USE_CXX14=ON'])
        #if self.compiler.cxx17_flag:
        #    options.extend(['-DDD4HEP_USE_CXX17=ON'])

        options.extend([
            '-DROOTSYS=%s' % spec['root'].prefix,
            '-DDD4HEP_USE_GEANT4=OFF',
            '-DDD4HEP_USE_XERCESC=ON',
            '-DXERCESC_ROOT_DIR=%s' % spec['xerces-c'].prefix,
            '-DCMAKE_CXX_STANDARD=17'
        ])

        return options

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('DD4hep_DIR', self.prefix)

    def url_for_version(self, version):
        url = "https://github.com/AIDASoft/DD4hep/archive/v{0}.tar.gz"

        if(version.up_to(1) < Version(10)):
                return url.format('0'+version.dashed.string)
        return url.format(version.dashed.string)
