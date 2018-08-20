from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class PhotosppToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('photospp')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'photospp.xml'
        contents = str("""
<tool name="photospp" version="${VER}">
  <lib name="Photospp"/>
  <lib name="PhotosppHepMC"/>
  <lib name="PhotosppHEPEVT"/>
  <client>
    <environment name="PHOTOSPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PHOTOSPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$PHOTOSPP_BASE/include"/>
  </client>
  <use name="hepmc"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)
