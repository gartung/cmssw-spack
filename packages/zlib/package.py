from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


# Although zlib comes with a configure script, it does not use Autotools
# The AutotoolsPackage causes zlib to fail to build with PGI
class Zlib(Package):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    homepage = "http://zlib.net"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://zlib.net/fossils/zlib-1.2.11.tar.gz"

    version('1.2.11', '1c9f62f0778697a09d36121ead88e08e')
    # Due to the bug fixes, any installations of 1.2.9 or 1.2.10 should be
    # immediately replaced with 1.2.11.
    version('1.2.8', '44d667c142d7cda120332623eab69f40')
    version('1.2.3', 'debc62758716a169df9f62e6ab2bc634')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('shared', default=True,
            description='Enables the build of shared libraries.')
    variant('optimize', default=True,
            description='Enable -O2 for a more optimized lib')

    patch('w_patch.patch', when="@1.2.11%cce")

    @property
    def libs(self):
        shared = '+shared' in self.spec
        return find_libraries(
            ['libz'], root=self.prefix, recursive=True, shared=shared
        )

    def setup_environment(self, spack_env, run_env):
        if '+pic' in self.spec:
            spack_env.append_flags('CFLAGS', self.compiler.pic_flag)
        if '+optimize' in self.spec:
            spack_env.append_flags('CFLAGS', '-O2')

    def install(self, spec, prefix):
        config_args = []
        if '~shared' in spec:
            config_args.append('--static')
        configure('--prefix={0}'.format(prefix), *config_args)

        make()
        if self.run_tests:
            make('check')
        make('install')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'zlib.xml'
        contents = str("""<tool name="zlib" version="$VER">
  <lib name="z"/>
  <client>
    <environment name="ZLIB_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$ZLIB_BASE/include"/>
    <environment name="LIBDIR" default="$$ZLIB_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)
