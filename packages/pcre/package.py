from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pcre(AutotoolsPackage):
    """The PCRE package contains Perl Compatible Regular Expression
    libraries. These are useful for implementing regular expression
    pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "http://www.pcre.org"
    url = "https://ftp.pcre.org/pub/pcre/pcre-8.40.tar.bz2"

    version('8.40', '41a842bf7dcecd6634219336e2167d1d')
    version('8.39', 'e3fca7650a0556a2647821679d81f585')
    version('8.38', '00aabbfe56d5a48b270f999b508c5ad2')

    patch('intel.patch', when='@8.38')

    variant('jit', default=False,
            description='Enable JIT support.')

    variant('utf', default=True,
            description='Enable support for UTF-8/16/32, '
            'incompatible with EBCDIC.')

    def configure_args(self):
        args = []

        if '+jit' in self.spec:
            args.append('--enable-jit')

        if '+utf' in self.spec:
            args.append('--enable-utf')
            args.append('--enable-unicode-properties')

        return args

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'pcre.xml'
        contents = str("""<tool name="pcre" version="$VER">
  <info url="http://www.pcre.org"/>
  <lib name="pcre"/>
  <client>
    <environment name="PCRE_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$PCRE_BASE/lib"/>
    <environment name="INCLUDE" default="$$PCRE_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="bz2lib"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)
