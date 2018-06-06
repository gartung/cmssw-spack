from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Xrootd(CMakePackage):
    """The XROOTD project aims at giving high performance, scalable fault
       tolerant access to data repositories of many kinds."""
    homepage = "http://xrootd.org"
    url = "http://xrootd.org/download/v4.6.0/xrootd-4.6.0.tar.gz"

    version('4.6.0', '5d60aade2d995b68fe0c46896bc4a5d1')
    version('4.5.0', 'd485df3d4a991e1c35efa4bf9ef663d7')
    version('4.4.1', '72b0842f802ccc94dede4ac5ab2a589e')
    version('4.4.0', '58f55e56801d3661d753ff5fd33dbcc9')
    version('4.3.0', '39c2fab9f632f35e12ff607ccaf9e16c')

    depends_on('cmake@2.6:', type='build')
    depends_on('python')


    @run_after('install')
    def write_scram_toolfiles(self):
        pyvers = str(self.spec['python'].version).split('.')
        pyver = pyvers[0] + '.' + pyvers[1]

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        values['PYVER'] = pyver

        fname = 'xrootd.xml'
        contents = str("""<tool name="xrootd" version="$VER">
  <lib name="XrdUtils"/>
  <lib name="XrdClient"/>
  <client>
    <environment name="XROOTD_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$XROOTD_BASE/include/xrootd"/>
    <environment name="INCLUDE" default="$$XROOTD_BASE/include/xrootd/private"/>
    <environment name="LIBDIR" default="$$XROOTD_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$XROOTD_BASE/bin" type="path"/>
  <runtime name="PYTHONPATH" value="$$XROOTD_BASE/lib/python${PYVER}/site-packages" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)
