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
            branch='cms/CORAL_2_3_21')

    depends_on('scram')
    depends_on('gmake')
    depends_on('cmssw-config')
    depends_on('coral-tool-conf')

    scram_arch = 'slc7_amd64_gcc700'
 
    def install(self, spec, prefix):
        scram = which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        scram_version = 'V%s' % spec['scram'].version
        project_dir = join_path(prefix, 'CORAL_%s' % self.version.underscored)

        with working_dir(build_directory, create=True):
            rsync = which('rsync')
            install_tree(source_directory,'src')
            install_tree(spec['cmssw-config'].prefix.bin,'config')
            with open('config/config_tag', 'w') as f:
                f.write('%s\n' % spec['cmssw-config'].version.underscored )
                f.close()
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep in spec.dependencies():
                xmlfiles = glob(join_path(dep.prefix.etc, 'scram.d', '*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile, 'tools/selected')
            uc=Executable('config/updateConfig.pl')
            uc(  '-p', 'CORAL',
                 '-v', 'CORAL_%s' % self.version.underscored,
                 '-s', scram_version,
                 '-t', build_directory,
                 '--keys', 'SCRAM_COMPILER=gcc',
                 '--keys', 'PROJECT_GIT_HASH=CORAL_%s' % self.version.underscored,
                 '--arch', '%s' % self.scram_arch)
            scram('project', '-d', '%s' % prefix, '-b', 'config/bootsrc.xml')

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
            relrelink('external')
            shutil.rmtree('tmp')

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
