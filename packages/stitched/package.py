from spack import *
import os,re


class Stitched(CMakePackage):
    homepage = "https://github.com/cms-sw/stitched.git"
    url = "https://github.com/cms-sw/stitched.git"

    version('master', git='https://github.com/cms-sw/Stitched.git',
            branch="master")
    
    resource(name='cmaketools', git='https://github.com/HSF/cmaketools.git',
              placement="cmaketools")
 
    depends_on('boost')
    depends_on('python')
    depends_on('py-pybind11', type=('link', 'run', 'test'))
    depends_on('tinyxml2')
    depends_on('md5-cms')
    depends_on('root ~opengl cxxstd=17')
    depends_on('xrootd')
    depends_on('clhep@2.4.1.3')
    depends_on('tbb')
    depends_on('cppunit', type=('link', 'test'))
    depends_on('xerces-c')
    depends_on('catch', type=('link', 'test'))
    depends_on('googletest', type=('link', 'test'))
    depends_on('benchmark@1.4.1', type=('link', 'test'))

    patch('stitched.patch')

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
        args.append('-DBUILDTEST=BOOL:True') 
        return args

    def setup_environment(self, spack_env, run_env):
        gcc = which(spack_cc)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.cc)

        spack_env.prepend_path('PATH',
                               join_path(self.build_directory, 'bin'))
        spack_env.prepend_path('PATH',
                               join_path(self.build_directory, 'test'))
        spack_env.prepend_path('LD_LIBRARY_PATH',
                               join_path(self.build_directory, 'lib'))
        spack_env.prepend_path('LD_LIBRARY_PATH',
                               join_path(self.build_directory, 'test'))
        spack_env.prepend_path('LD_LIBRARY_PATH',
                               join_path(self.spec['root'].prefix.lib))
        #spack_env.prepend_path('LD_LIBRARY_PATH',
        #                       join_path(gcc_prefix, 'lib64'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('PYTHONPATH',
                               join_path(self.build_directory, 'lib'))
        spack_env.prepend_path('PYTHONPATH',
                               join_path(self.build_directory, 'test'))
        spack_env.prepend_path('PYTHONPATH',
                               join_path(self.build_directory, 'python'))
        spack_env.prepend_path('PYTHONPATH',
                               join_path(self.build_directory, 'cfipython'))
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
        run_env.prepend_path('PYTHONPATH', '%s/python' % self.prefix)
        run_env.prepend_path('PYTHONPATH', '%s/cfipython' % self.prefix)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', '%s' % self.prefix)

