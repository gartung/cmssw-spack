from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class BlackhatToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('blackhat')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['blackhat'].version
        values['PFX'] = self.spec['blackhat'].prefix

        fname = 'blackhat.xml'
        contents = str("""
<tool name="blackhat" version="${VER}">
<lib name="Ampl_eval"/>
<lib name="BG"/>
<lib name="BH"/>
<lib name="BHcore"/>
<lib name="CutPart"/>
<lib name="Cut_wCI"/>
<lib name="Cuteval"/>
<lib name="Integrals"/>
<lib name="Interface"/>
<lib name="OLA"/>
<lib name="RatPart"/>
<lib name="Rateval"/>
<lib name="Spinors"/>
<lib name="assembly"/>
<lib name="ratext"/>
<client>
<environment name="BLACKHAT_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$BLACKHAT_BASE/lib/blackhat"/>
<environment name="INCLUDE" default="$$BLACKHAT_BASE/include"/>
</client>
<use name="qd"/>
<runtime name="WORKER_DATA_PATH" value="$$BLACKHAT_BASE/share/blackhat/datafiles/" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)
