from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class SqliteToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0.0', '', expand=False) 
    depends_on('sqlite')
    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['sqlite'].version
        values['PFX'] = self.spec['sqlite'].prefix
        fname = 'sqlite.xml'
        contents = str("""<tool name="sqlite" version="$VER">
  <lib name="sqlite3"/>
  <client>
    <environment name="SQLITE_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$SQLITE_BASE/lib"/>
    <environment name="BINDIR" default="$$SQLITE_BASE/bin"/>
    <environment name="INCLUDE" default="$$SQLITE_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)
