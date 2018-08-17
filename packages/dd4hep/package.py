from spack import *
import sys,os

class Dd4hep(CMakePackage):
    """software framework of the FCC project"""
    homepage = "https://github.com/AIDASoft/DD4hep/"
    url      = "https://github.com/AIDASoft/DD4hep/archive/v01-02.tar.gz"

    version('01.07', git='https://github.com/cms-externals/DD4hep.git',
             commit='ffe3645730224bf0b0a6dd6a8d2c6c1d87fa2b53')

    depends_on('cmake', type='build')
    depends_on('boost')
    depends_on('xerces-c')
    depends_on('root')
    depends_on('clhep')

    def cmake_args(self):
        spec = self.spec

        options = []

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
