from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class BerkeleyDb(AutotoolsPackage):
    """Oracle Berkeley DB"""

    homepage = "http://www.oracle.com/technetwork/database/database-technologies/berkeleydb/overview/index.html"
    url = "http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz"

    version('6.0.35', 'c65a4d3e930a116abaaf69edfc697f25')
    version('6.1.29', '7f4d47302dfec698fe088e5285c9098e')
    version('6.2.32', '33491b4756cb44b91c3318b727e71023')

    configure_directory = 'dist'
    build_directory = 'spack-build'

    def url_for_version(self, version):
        # newer version need oracle login, so get them from gentoo mirror
        return 'http://distfiles.gentoo.org/distfiles/db-{0}.tar.gz'.format(version)

    def configure_args(self):
        args = ['--disable-static', '--enable-cxx',
                '--enable-stl', '--disable-java', '--disable-tcl']
        return args

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'db6.xml'
        contents = str("""
<tool name="db6" version="${VER}">
  <lib name="db"/>
  <client>
    <environment name="DB6_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$DB6_BASE/lib"/>
    <environment name="INCLUDE" default="$$DB6_BASE/include"/>
    <environment name="BINDIR" default="$$DB6_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

