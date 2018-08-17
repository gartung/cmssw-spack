from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class HepmcToolfile(Package):
    depends_on("hepmc")

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['hepmc'].version
        values['PFX'] = self.spec['hepmc'].prefix
        fname = 'hepmc.xml'
        contents = str("""<tool name="HepMC" version="$VER">
  <lib name="HepMCfio"/>
  <lib name="HepMC"/>
  <client>
    <environment name="HEPMC_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$HEPMC_BASE/lib"/>
  </client>
  <use name="hepmc_headers"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$HEPMC_BASE/include" type="path"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

        fname = 'hepmc_headers.xml'
        contents = str("""<tool name="hepmc_headers" version="$VER">
  <client>
    <environment name="HEPMC_HEADERS_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$HEPMC_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)
