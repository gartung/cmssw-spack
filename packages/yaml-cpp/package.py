from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class YamlCpp(CMakePackage):
    """A YAML parser and emitter in C++"""

    homepage = "https://github.com/jbeder/yaml-cpp"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/yaml-cpp/0.5.1-oenich2/yaml-cpp-0.5.1.tar.gz"

    version('0.5.1', '0fa47a5ed8fedefab766592785c85ee7', preferred=True)

    depends_on('boost')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix,
            '-DBUILD_SHARED_LIBS=YES',
            '-DBoost_NO_SYSTEM_PATHS:BOOL=TRUE',
            '-DBoost_NO_BOOST_CMAKE:BOOL=TRUE',
            '-DBoost_ADDITIONAL_VERSIONS=1.57.0',
            '-DBOOST_ROOT:PATH=%s' % spec['boost'],
            '-DCMAKE_SKIP_RPATH=YES',
            '-DSKIP_INSTALL_FILES=1']
        return options

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'yamlcpp.xml'
        contents = str("""
<tool name="yaml-cpp" version="${VER}">
  <info url="http://code.google.com/p/yaml-cpp/"/>
  <lib name="yaml-cpp"/>
  <client>
    <environment name="YAML_CPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$YAML_CPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$YAML_CPP_BASE/include"/>
  </client>
  <use name="boost"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)
