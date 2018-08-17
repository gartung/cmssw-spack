from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GraphvizToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('graphviz')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        fname = 'graphviz.xml'
        contents = str("""<tool name="graphviz" version="$VER">
  <info url="http://www.research.att.com/sw/tools/graphviz/"/>
  <client>
    <environment name="GRAPHVIZ_BASE" default="$PFX"/>
  </client>
  <runtime name="PATH" value="$$GRAPHVIZ_BASE/bin" type="path"/>
  <use name="expat"/>
  <use name="zlib"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)
