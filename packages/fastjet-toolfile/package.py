from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FastjetToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('fastjet')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['fastjet'].version
        values['PFX'] = spec['fastjet'].prefix
        fname = 'fastjet.xml'
        contents = str("""<tool name="fastjet" version="$VER">
    <info url="http://www.lpthe.jussieu.fr/~salam/fastjet/"/>
    <lib name="fastjetplugins"/>
    <lib name="fastjettools"/>
    <lib name="siscone"/>
    <lib name="siscone_spherical"/>
    <lib name="fastjet"/>
    <client>
      <environment name="FASTJET_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$FASTJET_BASE/lib"/>
      <environment name="INCLUDE" default="$$FASTJET_BASE/include"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")

        write_scram_toolfile(contents, values, fname, prefix)
