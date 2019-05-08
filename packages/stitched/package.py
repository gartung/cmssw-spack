from spack import *
import os


class Stitched(CMakePackage):
    homepage = "https://github.com/gartung/stitched.git"
    url = "https://github.com/gartung/stitched.git"

    version('2019.5', git='https://github.com/gartung/stitched.git',
            tag='2019.5', submodules='True')

    depends_on('boost@:1.68.0')
    depends_on('python@:2.7.999')
    depends_on('py-pybind11')
    depends_on('tinyxml2')
    depends_on('md5-cms')
    depends_on('root')
    depends_on('xrootd')
    depends_on('clhep')
    depends_on('tbb')
    depends_on('cppunit')
    depends_on('xerces-c')

    def cmake_args(self):
        cxxstd = self.spec['root'].variants['cxxstd'].value
        args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path]
        args.append('-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix)
        args.append('-DBOOST_ROOT=%s' % self.spec['boost'].prefix)
        args.append('-DTBB_ROOT_DIR=%s' % self.spec['tbb'].prefix)
        args.append('-DTINYXMLROOT=%s' % self.spec['tinyxml2'].prefix)
        args.append('-DMD5ROOT=%s' % self.spec['md5-cms'].prefix)
        args.append('-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix)
        args.append('-DCMAKE_CXX_STANDARD={0}'.format(cxxstd))
        return args
