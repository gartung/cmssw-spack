from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class PhotosToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('photos')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['photos'].version
        values['PFX'] = spec['photos'].prefix

        fname = 'photos.xml'
        contents = str("""
<tool name="photos" version="${VER}">
  <lib name="photos"/>
  <client>
    <environment name="PHOTOS_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PHOTOS_BASE/lib"/>
  </client>
  <use name="photos_headers"/>
  <use name="f77compiler"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'photos_headers.xml'
        contents = str("""
<tool name="photos_headers" version="${VER}">
  <client>
    <environment name="PHOTOS_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$PHOTOS_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)
