from spack import *
import os,re


class Fwdata(CMakePackage):
    
    version('master', git='https://github.com/gartung/fwdata.git',
            branch="master")
    
    resource(name='cmaketools', git='https://github.com/HSF/cmaketools.git',
              placement="cmaketools")
 
    depends_on('boost')
    depends_on('root~opengl cxxstd=17')
    depends_on('python')
    depends_on('py-pybind11')
    depends_on('tinyxml2')
    depends_on('md5-cms')
    depends_on('uuid')
    depends_on('clhep@2.4.1.3')
    depends_on('tbb')
    depends_on('hepmc')
    depends_on('eigen')
    depends_on('fmt')
    depends_on('vdt')
    

    def cmake_args(self):
        cxxstd = self.spec['root'].variants['cxxstd'].value
        args = ['-DCMAKE_CXX_STANDARD=%s' % cxxstd]
        args.append('-DCMakeTools_DIR=%s/cmaketools'  % self.stage.source_path)
        args.append('-DBoost_INCLUDE_DIR=%s' % self.spec['boost'].prefix.include)
        args.append('-DROOT_DIR=%s' % self.spec['root'].prefix.cmake)
        args.append('-DTINYXMLROOT2=%s' % self.spec['tinyxml2'].prefix)
        args.append('-DTBB_ROOT_DIR=%s' % self.spec['intel-tbb'].prefix)
        args.append('-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix)
        args.append('-DHEPMC_ROOT_DIR=%s' % self.spec['hepmc'].prefix)
        args.append('-DUUID_ROOT_DIR=%s' % self.spec['uuid'].prefix)
        args.append('-DMD5ROOT=%s' % self.spec['md5-cms'].prefix)
        args.append('-DFMT_INCLUDE_DIR=%s' % self.spec['fmt'].prefix)
        args.append('-DEIGEN_INCLUDE_DIR=%s' % self.spec['eigen'].prefix) 
        args.append('-DVDT_ROOT_DIR=%s' % self.spec['vdt'].prefix)
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
        spack_env.prepend_path('LD_LIBRARY_PATH',
                               join_path(gcc_prefix, 'lib64'))
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
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.src)
        run_env.prepend_path('ROOT_INCLUDE_PATH', '%s' % self.prefix)

