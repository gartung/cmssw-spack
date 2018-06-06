from spack import *
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pythia6(Package):
    """PYTHIA is a program for the generation of high-energy physics events,
    i.e. for the description of collisions at high energies between elementary
    particles such as e+, e-, p and pbar in various combinations."""

    homepage = "https://pythia6.hepforge.org/"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia6/pythia6-426-src.tgz"

    version('426', '4dd75f551b7660c35f817c063abd74ca91b70259c0987905a06ebb2d21bcdf26')

    def install(self, spec, prefix):
        with working_dir(self.version.string):
            configure('--with-hepevt=4000')
            make()
            make('install')
            du.copy_tree('lib',prefix.lib)
            du.copy_tree('include',prefix.include)

    def url_for_version(self,version):
        url='http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia6/pythia6-426-src.tgz'%self.version
        return url

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'pythia6_headers.xml'
        contents = str("""
<tool name="pythia6_headers" version="${VER}">
  <client>
    <environment name="PYTHIA6_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$PYTHIA6_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

        fname = 'pythia6.xml'
        contents = str("""
<tool name="pythia6" version="${VER}">
  <lib name="pythia6"/>
  <lib name="pythia6_dummy"/>
  <lib name="pythia6_pdfdummy"/>
  <client>
    <environment name="PYTHIA6_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PYTHIA6_BASE/lib"/>
  </client>
  <use name="pythia6_headers"/>
  <use name="f77compiler"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

        fname = 'pydata.xml'
        contents = str("""
<tool name="pydata" version="${VER}">
  <client>
    <environment name="PYDATA_BASE" default="${PFX}"/>
  </client>
  <architecture name="slc.*|fc.*|linux*">
    <flags LDFLAGS="$$(PYDATA_BASE)/lib/pydata.o"/>
  </architecture>
  <flags NO_RECURSIVE_EXPORT="1"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)
