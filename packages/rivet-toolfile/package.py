from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class RivetToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('rivet')

    def install(self, spec, prefix):
        values={}
        values['VER']=spec['rivet'].version
        values['PFX']=spec['rivet'].prefix
        fname='rivet.xml'
        contents = str("""
<tool name="rivet" version="${VER}">
<lib name="Rivet"/>
<client>
<environment name="RIVET_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$RIVET_BASE/lib"/>
<environment name="INCLUDE" default="$$RIVET_BASE/include"/>
</client>
<runtime name="PATH" value="$$RIVET_BASE/bin" type="path"/>
<runtime name="RIVET_ANALYSIS_PATH" value="$$RIVET_BASE/lib" type="path"/>
<runtime name="PDFPATH" default="$$RIVET_BASE/share" type="path"/>
<runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
<runtime name="TEXMFHOME" value="$$RIVET_BASE/share/Rivet/texmf" type="path"/>
<use name="hepmc"/>
<use name="fastjet"/>
<use name="gsl"/>
<use name="yoda"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)
