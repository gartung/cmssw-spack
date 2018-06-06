from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Classlib(AutotoolsPackage):


    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/classlib/3.1.3/classlib-3.1.3.tar.bz2"

    version('3.1.3', '9114995676f4378e56ebacdd21220598')

    patch('classlib-3.1.3-fix-gcc47-cxx11.patch')
    patch('classlib-3.1.3-fix-obsolete-CLK_TCK.patch')
    patch('classlib-3.1.3-fix-unwind-x86_64.patch')
    patch('classlib-3.1.3-gcc46.patch')
    patch('classlib-3.1.3-memset-fix.patch')
    patch('classlib-3.1.3-sl6.patch')


    depends_on('bzip2')
    depends_on('pcre')
    depends_on('xz')
    depends_on('openssl')
    depends_on('zlib')

    def configure_args(self):
        args = ['--with-zlib-includes=%s' % self.spec['zlib'].prefix.include,
                '--with-zlib-libraries=%s' % self.spec['zlib'].prefix.lib,
                '--with-bz2lib-includes=%s' % self.spec['bzip2'].prefix.include,
                '--with-bz2lib-libraries=%s' % self.spec['bzip2'].prefix.lib,
                '--with-pcre-includes=%s' % self.spec['pcre'].prefix.include,
                '--with-pcre-libraries=%s' % self.spec['pcre'].prefix.lib,
                '--with-openssl-includes=%s' % self.spec['openssl'].prefix.include,
                '--with-openssl-libraries=%s' % self.spec['openssl'].prefix.lib,
                '--with-lzma-includes=%s' % self.spec['xz'].prefix.include,
                '--with-lzma-libraries=%s' % self.spec['xz'].prefix.lib]
        return args

    @run_before('build')
    def patch_makefile(self):
        perl = which('perl')
        perl('-p', '-i', '-e',
             's{-llzo2}{}g;!/^\S+: / ' +
             '&& s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g',
             'Makefile')

    def build(self, spec, prefix):
        make('CXXFLAGS=-Wno-error -ansi -pedantic -W -Wall -Wno-long-long ')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'classlib.xml'

        contents = str("""<tool name="classlib" version="$VER">
    <info url="http://cmsmac01.cern.ch/~lat/exports/"/>
    <client>
      <environment name="CLASSLIB_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$CLASSLIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$CLASSLIB_BASE/include"/>
      <flags CPPDEFINES="__STDC_LIMIT_MACROS"/>
      <flags CPPDEFINES="__STDC_FORMAT_MACROS"/>
      <lib name="classlib"/>
      <use name="zlib"/>
      <use name="bz2lib"/>
      <use name="pcre"/>
      <use name="openssl"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")
        write_scram_toolfile(contents, values, fname)
