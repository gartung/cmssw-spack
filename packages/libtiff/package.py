from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Libtiff(AutotoolsPackage):
    """libtiff graphics format library"""
    homepage = "http://www.simplesystems.org/libtiff/"
    url = "http://download.osgeo.org/libtiff/tiff-4.0.8.tar.gz"

    version('4.0.8', '2a7d1c1318416ddf36d5f6fa4600069b')
    version('4.0.7', '77ae928d2c6b7fb46a21c3a29325157b')
    version('4.0.6', 'd1d2e940dea0b5ad435f21f03d96dd72')
    version('4.0.3', '051c1068e6a0627f461948c365290410')

    depends_on('cmssw.libjpeg-turbo')
    depends_on('zlib')
    depends_on('xz')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'libtiff.xml'
        contents = str("""<tool name="libtiff" version="$VER">
  <info url="http://www.libtiff.org/"/>
  <lib name="tiff"/>
  <client>
    <environment name="LIBTIFF_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBTIFF_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBTIFF_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="libjpeg-turbo"/>
  <use name="zlib"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)
