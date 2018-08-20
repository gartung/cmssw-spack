from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ClasslibToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('classlib')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['classlib'].version
        values['PFX'] = spec['classlib'].prefix

        fname = 'classlib.xml'

        contents = str("""<tool name="classlib" version="$VER">
    <info url="http://cmsmac01.cern.ch/~lat/exports/"/>
    <client>
      <environment name="CLASSLIB_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$CLASSLIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$CLASSLIB_BASE/include"/>
      <flags CPPDEFINES="__STDC_LIMIT_MACROS"/>
      <flags CPPDEFINES="__STDC_FORMAT_MACROS"/>
      <lib name="classlib"/>
      <use name="zlib"/>
      <use name="bz2lib"/>
      <use name="pcre"/>
      <use name="openssl"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")
        write_scram_toolfile(contents, values, fname, prefix)
