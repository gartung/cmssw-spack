from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pythia6Toolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('pythia6')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['pythia6'].version
        values['PFX'] = spec['pythia6'].prefix

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

        write_scram_toolfile(contents, values, fname, prefix)

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

        write_scram_toolfile(contents, values, fname, prefix)

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

        write_scram_toolfile(contents, values, fname, prefix)
