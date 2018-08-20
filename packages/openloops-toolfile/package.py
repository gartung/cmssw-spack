from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class OpenloopsToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('openloops')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        fname = 'openloops.xml'
        contents = str("""
<tool name="openloops" version="${VER}">
<client>
<environment name="OPENLOOPS_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$OPENLOOPS_BASE/lib"/>
<runtime name="CMS_OPENLOOPS_PREFIX" value="$$OPENLOOPS_BASE" type="path"/>
</client>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)
