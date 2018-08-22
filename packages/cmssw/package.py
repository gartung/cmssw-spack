from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
from spack.util.executable import Executable
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import relrelink


class Cmssw(Package):
    """CMSSW built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/cms-sw/cmssw/archive/CMSSW_10_2_0.tar.gz"

    version('10.2.0', git='https://github.com/cms-sw/cmssw.git', tag='CMSSW_10_2_0')

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        version_underscore = str(self.version).replace('.', '_')
        return "https://github.com/cms-sw/cmssw/archive/CMSSW_%s.tar.gz" % version_underscore

    depends_on('scram')
    depends_on('cmssw-config')
    depends_on('cmssw-tool-conf')
    depends_on('gmake')
    depends_on('llvm')
 
    if sys.platform == 'darwin':
        patch('macos.patch')
    else:
        patch('linux.patch')

    scram_arch = 'slc7_amd64_gcc700'

    def install(self, spec, prefix):
        scram = Executable(spec['scram'].prefix.bin+'/scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        scram_version = 'V%s' % spec['scram'].version
        project_dir = join_path(prefix, cmssw_u_version)

        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        values = {}
        values['SELF_LIB'] = project_dir + '/lib/' + self.scram_arch
        values['SELF_INC'] = project_dir + '/src'
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()
        with working_dir(build_directory, create=True):
            install_tree(source_directory, 'src',
                         ignore=shutil.ignore_patterns('spack_build.*',
                                                       '.git', 'config'))
            install_tree(spec['cmssw-config'].prefix.bin, 'config',
                         ignore=shutil.ignore_patterns('.git'))
            config_tag = spec['cmssw-config'].version
            with open('config/config_tag', 'w') as f:
                f.write(config_tag+'\n')
                f.close()
            #mkdirp('tools/selected')
            #mkdirp('tools/available')
            #for dep in spec.dependencies():
            #    xmlfiles = glob(join_path(dep.prefix.etc, 'scram.d', '*.xml'))
            #    for xmlfile in xmlfiles:
            #        install(xmlfile, 'tools/selected')
            uc = Executable('config/updateConfig.pl')
            uc('-p', 'CMSSW',
                 '-v', '%s' % cmssw_u_version,
                 '-s', '%s' % scram_version,
                 '-t', '%s' % self.spec['cmssw-tool-conf'].prefix,
                 '--keys', 'SCRAM_COMPILER=gcc',
                 '--keys', 'PROJECT_GIT_HASH=' + cmssw_u_version,
                 '--arch', '%s' % self.scram_arch)
            scram('project', '-d', prefix, '-b', 'config/bootsrc.xml')

        with working_dir(project_dir, create=False):
            matches = []

            for f in glob('src/*/*/test/BuildFile*'):
                matches.append(f)
            for m in matches:
                if os.path.exists(m):
                    os.remove(m)

            scram.add_default_env('LOCALTOP', project_dir)
            scram.add_default_env('CMSSW_BASE', project_dir)
            scram.add_default_env(
                'LD_LIBRARY_PATH', project_dir + '/lib/' + self.scram_arch)
            scram.add_default_env(
                'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
            scram.add_default_env(
                'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)
            scram('build', '-v', '-k', '-j8')
            relrelink('external')
            shutil.rmtree('tmp')
#            install_tree(project_dir,prefix)


#        with working_dir(join_path(prefix,cmssw_u_version), create=False):
#            os.environ[ 'LOCALTOP' ] = os.getcwd()
#            os.environ[ 'RELEASETOP' ] = os.getcwd()
#            os.environ[ 'CMSSW_RELEASE_BASE' ] = os.getcwd()
#            os.environ[ 'CMSSW_BASE' ] = os.getcwd()
#            scram('build', 'ProjectRename')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        spack_env.set('LOCALTOP', self.prefix + '/' + cmssw_u_version)
        spack_env.set('RELEASETOP', self.prefix + '/' + cmssw_u_version)
        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix +
                              '/' + cmssw_u_version + '/lib/' + self.scram_arch)
        spack_env.append_path(
            'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)

    def setup_environment(self, spack_env, run_env):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        spack_env.set('LOCALTOP', self.prefix + '/' + cmssw_u_version)
#        spack_env.set('RELEASETOP', self.prefix+'/'+cmssw_u_version)
#        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix +
                              '/' + cmssw_u_version + '/lib/' + self.scram_arch)
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
        spack_env.append_path(
            'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)

