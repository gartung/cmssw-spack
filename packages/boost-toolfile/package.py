from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class BoostToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('boost')

    def install(self, spec, prefix):

        values = {}
        values['VER'] = spec['boost'].version
        values['PFX'] = spec['boost'].prefix

        fname = 'boost.xml'
        contents = str("""<tool name="boost" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_thread"/>
  <lib name="boost_signals"/>
  <lib name="boost_date_time"/>
  <client>
    <environment name="BOOST_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$BOOST_BASE/lib"/>
    <environment name="INCLUDE" default="$$BOOST_BASE/include"/>
  </client>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$BOOST_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags CPPDEFINES="BOOST_SPIRIT_THREADSAFE PHOENIX_THREADSAFE _LIBCPP_ENABLE_CXX17_REMOVED_FEATURES=1"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_chrono toolfile
        fname = 'boost_chrono.xml'
        contents = str("""<tool name="boost_chrono" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_chrono"/>
  <use name="boost_system"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_filesystem toolfile
        fname = 'boost_filesystem.xml'
        contents = str("""<tool name="boost_filesystem" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_filesystem"/>
  <use name="boost_system"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_system toolfile
        fname = 'boost_system.xml'
        contents = str("""<tool name="boost_system" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_system"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_program_options toolfile
        fname = 'boost_program_options.xml'
        contents = str("""<tool name="boost_program_options" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_program_options"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_python toolfile
        fname = 'boost_python.xml'
        contents = str("""
<tool name="boost_python" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_python"/>
  <client>
    <environment name="BOOST_PYTHON_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$BOOST_PYTHON_BASE/lib"/>
    <environment name="INCLUDE" default="$$BOOST_PYTHON_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="python"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_regex toolfile
        fname = 'boost_regex.xml'
        contents = str("""<tool name="boost_regex" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_regex"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_signals toolfile
        fname = 'boost_signals.xml'
        contents = str("""<tool name="boost_signals" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_signals"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'boost_serialization.xml'
        contents = str("""<tool name="boost_serialization" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_serialization"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'boost_test.xml'
        contents = str("""<tool name="boost_test" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_unit_test_framework"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'boost_iostreams.xml'
        contents = str("""<tool name="boost_iostreams" version="$VER">
  <info url="http://www.boost.org"/>
  <lib name="boost_iostreams"/>
  <use name="boost"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# boost_header toolfile
        fname = 'boost_header.xml'
        contents = str("""<tool name="boost_header" version="$VER">
  <info url="http://www.boost.org"/>
  <client>
    <environment name="BOOSTHEADER_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$BOOSTHEADER_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)
