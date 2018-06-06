from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Yoda(Package):
    homepage = "http://www.example.com"
    url = "http://cern.ch/service-spi/external/MCGenerators/distribution/yoda/yoda-1.6.5-src.tgz"

    version('1.6.5', '634fa27412730e511ca3d4c67f6086e7')


    depends_on('root')
    depends_on('python')
    depends_on('py-cython', type='build')

    def install(self, spec, prefix):
        with working_dir(str(self.spec.version), create=False):
            configure('--enable-root', '--prefix=%s' % self.prefix)
            make('all')
            make('install')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'yoda.xml'
        contents = str("""
<tool name="yoda" version="${VER}">
  <lib name="YODA"/>
  <client>
    <environment name="YODA_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$YODA_BASE/lib"/>
    <environment name="INCLUDE" default="$$YODA_BASE/include"/>
  </client>
  <use name="root_cxxdefaults"/>
  <runtime name="PYTHONPATH" value="$$YODA_BASE/lib/python2.7/site-packages" type="path"/>
  <runtime name="PATH"       value="$$YODA_BASE/bin" type="path"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)
