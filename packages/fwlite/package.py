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

    version('9_2_15', 'b587e111bc072dcfc7be679f6783f966')

    config_tag = 'V05-05-40'

    resource(name='config',
             url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/fwlite/CMSSW_9_2_12_FWLITE/%s.tar.gz' % config_tag,
             md5='87af022eba2084d0db2b4d92245c3629',
             destination='.',
             placement='config'
             )


    depends_on('scram')
    depends_on('gmake-toolfile')
    depends_on('root-toolfile')
    depends_on('intel-tbb-toolfile')
    depends_on('tinyxml-toolfile')
    depends_on('clhep-toolfile')
    depends_on('md5-toolfile')
    depends_on('python-toolfile+shared')
    depends_on('vdt-toolfile')
    depends_on('boost-toolfile')
    depends_on('libsigcpp-toolfile')
    depends_on('xrootd-toolfile')
    depends_on('cppunit-toolfile')
    depends_on('xerces-c-toolfile')
    depends_on('expat-toolfile')
    depends_on('sqlite-toolfile')
    depends_on('bzip2-toolfile')
    depends_on('gsl-toolfile')
    depends_on('hepmc-toolfile')
    depends_on('libpng-toolfile')
    depends_on('giflib-toolfile')
    depends_on('openssl-toolfile')
    depends_on('pcre-toolfile')
    depends_on('zlib-toolfile')
    depends_on('xz-toolfile')
    depends_on('libtiff-toolfile')
    depends_on('libjpeg-turbo-toolfile')
    depends_on('libxml2-toolfile')
    depends_on('bzip2-toolfile')
    depends_on('fireworks-geometry-toolfile')
    depends_on('llvm-toolfile')
    depends_on('uuid-cms-toolfile')

    if sys.platform == 'darwin':
        patch('macos.patch')
    else:
        patch('linux.patch')

    scram_arch = 'linux_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'


    def install(self, spec, prefix):
        scram = which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        scram_version = 'V' + str(spec['scram'].version)

        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        with working_dir(build_directory, create=True):
            install_tree(source_directory, 'src', 
                        ignore=shutil.ignore_patterns('spack_build.out',
                                                      'spack_build.env', 
                                                       '.git', 'config')) 
            install_tree(join_path(source_directory, 'config'), 'config', 
                         ignore=shutil.ignore_patterns('.git')) 

            install(join_path(os.path.dirname(__file__), "fwlite_build_set.file"),
                "fwlite_build_set.file")

            with open('config/config_tag', 'w') as f:
                f.write(self.config_tag)
                f.close()

            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep in spec.dependencies():
                xmlfiles = glob(join_path(dep.prefix.etc, 'scram.d', '*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile, 'tools/selected')

            perl = which('perl')
            perl('config/updateConfig.pl',
                 '-p', 'CMSSW',
                 '-v', self.cmssw_u_version,
                 '-s', scram_version,
                 '-t', build_directory,
                 '--keys', 'SCRAM_COMPILER=gcc',
                 '--keys', 'PROJECT_GIT_HASH=' + self.cmssw_u_version,
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
            scram('project', '-d', prefix, '-b', 'config/bootsrc.xml')

        with working_dir(join_path(prefix, self.cmssw_u_version), create=False):
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

            scram('build', '-v', '-k', '-j8')
            relrelink('external')
            shutil.rmtree('tmp')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LOCALTOP', join_path(self.prefix,self.cmssw_u_version))
        spack_env.set('RELEASETOP', join_path(self.prefix,self.cmssw_u_version))
        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', join_path(self.prefix,
                              self.cmssw_u_version,'/lib/',self.scram_arch))

    def setup_environment(self, spack_env, run_env):
        spack_env.set('LOCALTOP', join_path(self.prefix, self.cmssw_u_version))
        spack_env.set('RELEASETOP', join_path(self.prefix, self.cmssw_u_version))
        spack_env.set('CMSSW_RELEASE_BASE', join_path(self.prefix, self.cmssw_u_version))
        spack_env.set('CMSSW_BASE', join_path(self.prefix, self.cmssw_u_version))
        spack_env.append_path('LD_LIBRARY_PATH', join_path(self.prefix,
                              self.cmssw_u_version, '/lib/', self.scram_arch))
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        self.set_version()
        return "https://github.com/cms-sw/cmssw/archive/%s.tar.gz" % self.cmssw_u_version

    def set_version(self):
        self.cmssw_version = 'CMSSW.' + str(self.version)
        self.cmssw_u_version = self.cmssw_version.replace('.', '_')
