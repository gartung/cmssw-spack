from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class QdToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('qd')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['qd'].version
        values['PFX'] = spec['qd'].prefix

        fname = 'qd.xml'
        contents = str("""
<tool name="qd" version="${VER}">
<lib name="qd_f_main"/>
<lib name="qdmod"/>
<lib name="qd"/>
<client>
<environment name="QD_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$QD_BASE/lib"/>
<environment name="INCLUDE" default="$$QD_BASE/include"/>
</client>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)
