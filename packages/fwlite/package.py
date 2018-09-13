from spack import *
from glob import glob
import re
import fnmatch
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile, relrelink


class Fwlite(Package):
    """CMSSW FWLite built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/cms-sw/cmssw/archive/CMSSW_9_2_15.tar.gz"

    version('10.2.4', git='https://github.com/cms-sw/cmssw.git', tag='CMSSW_10_2_4')

    depends_on('scram')
    depends_on('cmssw-config')
    depends_on('fwlite-tool-conf')
    depends_on('gmake')
    depends_on('llvm')

    if sys.platform == 'darwin':
        patch('macos.patch')
    else:
        patch('linux.patch')

    scram_arch = 'linux_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'


    def install(self, spec, prefix):
        scram = which('scram')
        source_directory = self.stage.source_path
        build_directory=os.path.realpath(self.stage.path)
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        scram_version = 'V%s' % spec['scram'].version
        config_tag = '%s' % spec['cmssw-config'].version


#        gcc = which(spack_f77)
#        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
#        gcc_machine = gcc('-dumpmachine', output=str)
#        gcc_ver = gcc('-dumpversion', output=str)

        with working_dir(build_directory):
            install_tree(source_directory, 'src',
                         ignore=shutil.ignore_patterns('spack_build.*',
                                                       '.git', 'config'))
            install_tree(spec['cmssw-config'].prefix.bin, 'config', 
                         ignore=shutil.ignore_patterns('.git')) 

            with open('config/config_tag', 'w') as f:
                f.write(config_tag+'\n')
                f.close()

            install(join_path(os.path.dirname(__file__), "fwlite_build_set.file"),
                "fwlite_build_set.file")

            uc = Executable('config/updateConfig.pl')
            uc('-p', 'CMSSW',
                 '-v', cmssw_u_version,
                 '-s', scram_version,
                 '-t', '%s' % spec['fwlite-tool-conf'].prefix,
                 '--keys', 'SCRAM_COMPILER=gcc',
                 '--keys', 'PROJECT_GIT_HASH=%s'%cmssw_u_version,
                 '--arch', self.scram_arch)
            fin = 'config/bootsrc.xml'
            matchexp = re.compile(
                r"(\s*\<download.*)(file:src)(.*)(name=\"src)(\"/\>)")
            lines = [line.rstrip('\n') for line in open(fin, 'r')]
            fout = open(fin, 'w')
            for line in lines:
                mobj = matchexp.match(line)
                if mobj:
                    replacement = '#' + line + '\n'
                    fout.write(replacement)
                    reps = [line.rstrip('\n') for line in open(
                        'fwlite_build_set.file', 'r')]
                    for rep in reps:
                        replacement = mobj.group(1) + mobj.group(2) + '/' + rep + mobj.group(
                            3) + mobj.group(4) + '/' + rep + mobj.group(5) + '\n'
                        fout.write(replacement)
                else:
                    replacement = line + '\n'
                    fout.write(replacement)
            fout.close()
            scram('project', '-d', '%s' %  build_directory, '-b', 'config/bootsrc.xml')
        project_dir =join_path(os.path.realpath(self.stage.path),cmssw_u_version)
        with working_dir(project_dir, create=False):
            matches = []
            matches.append('src/CommonTools/Utils/src/TMVAEvaluator.cc')
            matches.append(
                'src/FWCore/MessageLogger/python/MessageLogger_cfi.py')
            matches.append('src/CommonTools/Utils/plugins/GBRForestWriter.cc')

            for f in glob('src/*/*/test/BuildFile.xml'):
                matches.append(f)
            for m in matches:
                if os.path.exists(m):
                    os.remove(m)
            scram('setup', 'self')
            if sys.platform == 'darwin':
                scram('build', '-r', '-v', '-j8', 'COMPILER=llvm')
            else:
                scram('build', '-r', '-v', '-j8' )
            relrelink('external')
            shutil.rmtree('tmp')
        install_tree(project_dir,prefix+'/'+cmssw_u_version, symlinks=True)
        relrelink(prefix+'/'+cmssw_u_version+'external')


        with working_dir(join_path(prefix,cmssw_u_version), create=False):
#            os.environ[ 'LOCALTOP' ] = os.getcwd()
#            os.environ[ 'RELEASETOP' ] = os.getcwd()
#            os.environ[ 'CMSSW_RELEASE_BASE' ] = os.getcwd()
#            os.environ[ 'CMSSW_BASE' ] = os.getcwd()
            scram('build', 'ProjectRename')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
#        spack_env.set('LOCALTOP', join_path(self.prefix,cmssw_u_version))
#        spack_env.set('RELEASETOP', join_path(self.prefix,cmssw_u_version))
#        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
#        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', join_path(self.stage.path,
                              cmssw_u_version,'/lib/',self.scram_arch))

    def setup_environment(self, spack_env, run_env):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
#        spack_env.set('LOCALTOP', join_path(self.stage.path, cmssw_u_version))
#        spack_env.set('RELEASETOP', join_path(self.stage.path, cmssw_u_version))
#        spack_env.set('CMSSW_RELEASE_BASE', join_path(self.stage.path,cmssw_u_version))
#        spack_env.set('CMSSW_BASE', join_path(self.stage.path, cmssw_u_version))
#        spack_env.append_path('LD_LIBRARY_PATH', join_path(os.path.realpath(self.stage.path),
#                              cmssw_u_version, '/lib/', self.scram_arch))
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
