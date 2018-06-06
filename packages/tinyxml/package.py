from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Tinyxml(Package):

    homepage = "https://github.com/cms-externals/tinyxml"
    url = "http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/tinyxml/2.5.3-giojec/tinyxml.2.5.3-3b1ed8542a820e77de84bc08734bde904c3b12be.tgz"

    version('2.5.3', '3126b4a2dbfbd087e28faca4ad62cd31',
            url='http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/tinyxml/2.5.3-giojec/tinyxml.2.5.3-3b1ed8542a820e77de84bc08734bde904c3b12be.tgz')
    if sys.platform == 'darwin':
        patch('tinyxml.patch')

    depends_on('boost@1.63.0+python^python+shared')
    depends_on('gmake', type='build')

    def install(self, spec, prefix):
        gmake = which('gmake')
        gmake('BOOST_ROOT=%s' % spec['boost'].prefix)
        cp = which('cp')
        md = which('mkdir')
        md('%s' % self.prefix.lib)
        md('%s' % self.prefix.include)
        if sys.platform == 'darwin':
            cp('-v', 'libtinyxml.dylib', prefix.lib)
            fix_darwin_install_name(prefix.lib)
        else:
            cp('-v', 'libtinyxml.so', prefix.lib)
        cp('-v', 'tinystr.h', 'tinyxml.h', prefix.include)



    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'tinyxml.xml'
        contents = str("""<tool name="tinyxml" version="$VER">
  <info url="https://sourceforge.net/projects/tinyxml/"/>
   <lib name="tinyxml"/>
  <client>
    <environment name="TINYXML_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$TINYXML_BASE/lib"/>
    <environment name="INCLUDE" default="$$TINYXML_BASE/include"/>
  </client>  
</tool>""")

        write_scram_toolfile(contents, values, fname)
