from spack import *
import os


class Stitched(CMakePackage):
    homepage = "https://github.com/cms-sw/stitched.git"
    url = "https://github.com/cms-sw/stitched.git"

    version('master', git='https://github.com/cms-sw/stitched.git',
            branch="master")
    
    resource(name='cmaketools', git='https://github.com/HSF/cmaketools.git',
              placement="cmaketools")
 
    resource(name='buildfile2cmake', git='https://github.com/gartung/buildfile2cmake.git',
              placement="buildfile2cmake")

    depends_on('boost@:1.69.0')
    depends_on('python')
    depends_on('libpython2')
    depends_on('py-pybind11')
    depends_on('py-six')
    depends_on('py-future')
    depends_on('tinyxml2')
    depends_on('md5-cms')
    depends_on('root')
    depends_on('xrootd')
    depends_on('clhep')
    depends_on('tbb')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('catch')
    depends_on('googletest')
    depends_on('benchmark@1.4.1')

    @run_before('cmake')
    def createcmakefiles(self):
         with working_dir(self.stage.source_path):
           b2c=Executable('buildfile2cmake/buildfile2cmake')
           b2c()

    def cmake_args(self):
        cxxstd = self.spec['root'].variants['cxxstd'].value
        args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path]
        args.append('-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix)
        args.append('-DBOOST_ROOT=%s' % self.spec['boost'].prefix)
        args.append('-DTBB_ROOT_DIR=%s' % self.spec['tbb'].prefix)
        args.append('-DTINYXMLROOT2=%s' % self.spec['tinyxml2'].prefix)
        args.append('-DMD5ROOT=%s' % self.spec['md5-cms'].prefix)
        args.append('-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix)
        args.append('-DCMAKE_CXX_STANDARD=%s'% cxxstd)
        args.append('-DXROOTD_INCLUDE_DIR=%s/xrootd' % self.spec['xrootd'].prefix.include)
        args.append('-DCATCH2_INCLUDE_DIRS=%s/catch2' % self.spec['catch'].prefix.include)
        args.append('-DBUILDTEST=1') 
        return args

