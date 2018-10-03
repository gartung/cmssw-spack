from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import relrelink, write_scram_toolfile

class Coral(Package):
    """CORAL built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/cms-externals/coral.tgz"

    version('2.3.21', git='https://github.com/cms-externals/coral',
            commit='1a2014499b7459fa725f05ef5d0f2d9142eeb697')

    patch('coral-2_3_21-gcc8.patch')

    depends_on('scram')
    depends_on('gmake')
    depends_on('cmssw-config')
    depends_on('coral-tool-conf')

    scram_arch = 'slc_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'
 
    def install(self, spec, prefix):
        coral_version = 'CORAL.' + str(self.version)
        coral_u_version = coral_version.replace('.', '_')

        scram = Executable(spec['scram'].prefix.bin+'/scram')        
        source_directory = self.stage.source_path
        scram_version = 'V%s' % spec['scram'].version

        config_tag = '%s' % spec['cmssw-config'].version.underscored 
        with working_dir(self.stage.path):
            install_tree(source_directory,'src')
            install_tree(spec['cmssw-config'].prefix.bin, 'config')
            with open('config/config_tag', 'w') as f:
                f.write(config_tag+'\n' )
                f.close()

            uc=Executable('config/updateConfig.pl')
            uc(  '-p', 'CORAL',
                 '-v', '%s' % coral_u_version,
                 '-s', '%s' % scram_version,
                 '-t', '%s' % spec['coral-tool-conf'].prefix,
                 '--keys', 'SCRAM_COMPILER=gcc',
                 '--keys', 'PROJECT_GIT_HASH=' + coral_u_version,
                 '--arch', '%s' % self.scram_arch)
            scram('project', '-d', os.path.realpath(self.stage.path), '-b', 'config/bootsrc.xml')

        project_dir = os.path.realpath(self.stage.path+'/'+coral_u_version)
        with working_dir(project_dir, create=False):
            matches = []

            for f in glob('src/*/*/test/BuildFile*'):
                matches.append(f)
            for m in matches:
                if os.path.exists(m):
                    os.remove(m)

            scram.add_default_env('LOCALTOP', project_dir)
            scram.add_default_env('CORAL_BASE', project_dir)
            scram.add_default_env('LD_LIBRARY_PATH', '%s/lib/%s' %
                                  (project_dir, self.scram_arch))
            scram('build', '-v', '-j8')
            shutil.rmtree('external')
            shutil.rmtree('tmp')
            os.remove('slc_amd64_gcc/python/LCG/PyCoral')
        install_tree(project_dir, prefix+'/'+coral_u_version)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('CORAL_RELEASE_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', '%s/CORAL_%s/%s/lib' %
                              (self.prefix, self.version.underscored, self.scram_arch))

    def setup_environment(self, spack_env, run_env):
        spack_env.set('LOCALTOP', self.prefix + '/' +
                      self.version.underscored.string)
        spack_env.set('CORAL_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', '%s/CORAL_%s/%s/lib' %
                              (self.prefix, self.version.underscored, self.scram_arch))

    @run_after('install')
    def make_links(self):
        with working_dir(self.spec.prefix):
            os.symlink('CORAL_%s/include/LCG' % self.version.underscored, 'include')
            os.symlink('CORAL_%s/%s/lib' % (self.version.underscored, self.scram_arch), 'lib')
