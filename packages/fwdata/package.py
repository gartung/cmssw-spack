from spack import *
import os,re


class Fwdata(CMakePackage):
    
    version('12.4.0.p2', git='https://github.com/gartung/fwdata.git',
            branch="master", commit="4c37c02fe358fed80ffd7fe00cf8b21340c0d52f")
    
    resource(name='cmaketools', git='https://github.com/gartung/cmaketools.git',
              placement="cmaketools", commit='ad8d834351033ab627752e35a252b69e52881042')
 
    depends_on('boost')
    depends_on('root~opengl~x')
    depends_on('python')
    depends_on('py-pybind11')
    depends_on('tinyxml2')
    depends_on('md5-cms')
    depends_on('uuid')
    depends_on('clhep@2.4.4.0')
    depends_on('intel-tbb')
    depends_on('hepmc@2.6.10')
    depends_on('eigen')
    depends_on('fmt')
    depends_on('vdt')
    depends_on('hls')
    patch('nls.patch')

    def patch(self):
        if '^intel-tbb-oneapi@2021.1:' in self.spec:
        # TBB 2021+ is built with cmake and provides TBBConfig.cmake
            os.remove('cmaketools/modules/FindTBB.cmake')
            os.remove('cmaketools/modules/FindCLHEP.cmake')
 

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
        args.append('-DCMSMD5ROOT=%s' % self.spec['md5-cms'].prefix)
        args.append('-DFMT_INCLUDE_DIR=%s' % self.spec['fmt'].prefix)
        args.append('-DEIGEN_INCLUDE_DIR=%s' % self.spec['eigen'].prefix) 
        args.append('-DVDT_ROOT_DIR=%s' % self.spec['vdt'].prefix)
        args.append('-DHLS_INCLUDE_DIR=%s' % self.spec['hls'].prefix)
        args.append('-DTBB_LIBRARIES=TBB::tbb')
        args.append('-DCLHEP_LIBRARIES=CLHEP::CLHEP')
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

