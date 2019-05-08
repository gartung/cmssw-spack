from spack import *
import os


class Stitched(CMakePackage):
    homepage = "https://github.com/gartung/stitched.git"
    url = "https://github.com/gartung/stitched.git"

    version('10.5.X', git='https://github.com/gartung/stitched.git',
            commit='bdab7ca1b3c65bd96482e277c3614c02ae625203', submodules='True')

    depends_on('boost+python@1.67.0')
    depends_on('python')
    depends_on('tinyxml2')
    depends_on('md5')
    depends_on('root')
    depends_on('clhep')
    depends_on('tbb')
    depends_on('cppunit')

    def cmake_args(self):
        args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path]
        args.append('-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix)
        args.append('-DBOOST_ROOT=%s' % self.spec['boost'].prefix)
        args.append('-DTBB_ROOT_DIR=%s' % self.spec['tbb'].prefix)
        args.append('-DTINYXMLROOT=%s' % self.spec['tinyxml2'].prefix)
        args.append('-DMD5ROOT=%s' % self.spec['md5'].prefix)
        args.append('-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix)
        return args
