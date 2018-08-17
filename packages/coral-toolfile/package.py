from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import relrelink, write_scram_toolfile


class CoralToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'   
    version('1.0', '', expand=False)
    depends_on('coral')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['coral'].version
        values['PFX'] = self.spec['coral'].prefix
        values['UVER'] = 'CORAL_%s' % self.spec['coral'].version.underscored

        fname = 'coral.xml'
        contents = str("""
<tool name="coral" version="${VER}" type="scram">
  <client>
    <environment name="CORAL_BASE" default="${PFX}/${UVER}"/>
    <environment name="LIBDIR" default="$$CORAL_BASE/$$SCRAM_ARCH/lib"/>
    <environment name="INCLUDE" default="$$CORAL_BASE/include/LCG"/>
  </client>
  <runtime name="PYTHONPATH" default="$$CORAL_BASE/$$SCRAM_ARCH/python" type="path"/>
  <runtime name="PYTHONPATH" default="$$CORAL_BASE/$$SCRAM_ARCH/lib" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)
