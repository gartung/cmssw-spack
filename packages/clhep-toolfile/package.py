from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ClhepToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('clhep')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['clhep'].version
        values['PFX'] = self.spec['clhep'].prefix

        fname = 'clhep.xml'
        contents = str("""<tool name="clhep" version="$VER">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <lib name="CLHEP"/>
  <client>
    <environment name="CLHEP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$CLHEP_BASE/lib"/>
    <environment name="INCLUDE" default="$$CLHEP_BASE/include"/>
  </client>
  <runtime name="CLHEP_PARAM_PATH" value="$$CLHEP_BASE"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$CLHEP_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

        fname = 'clhepheader.xml'
        contents = str("""<tool name="clhepheader" version="$VER">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <client>
    <environment name="CLHEPHEADER_BASE" default="$PFX"/>
    <environment name="INCLUDE"    default="$$CLHEPHEADER_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)
