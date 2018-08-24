from spack import *
import os


class Stitched(CMakePackage):
    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.2.3.tar.gz"

    version('8.0.X', git='https://github.com/gartung/stitched.git',
            commit='8ce0c76', submodules='True')

    depends_on('boost+python')
    depends_on('python')
    depends_on('tinyxml')
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
        args.append('-DTINYXMLROOT=%s' % self.spec['tinyxml'].prefix)
        args.append('-DMD5ROOT=%s' % self.spec['md5'].prefix)
        args.append('-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix)
        return args
