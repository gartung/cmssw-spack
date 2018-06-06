from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class Cython(Package):



    homepage = "http://www.example.com"
    url = "http://cern.ch/service-spi/external/MCGenerators/distribution/cython/cython-0.22-src.tgz"

    version('0.22', 'f7653aaae762593e13a66f94dadf1835')

    depends_on('python', type=('build', 'run'))

    extends('python')

    def install(self, spec, prefix):
        with working_dir(str(spec.version)):
            python = which('python')
            python('setup.py', 'build')
            python('setup.py', 'install', '--prefix=%s' % prefix)

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'cython.xml'
        contents = str("""
<tool name="cython" version="${VER}">
  <client>
    <environment name="CYTHON_BASE" default="${PFX}"/>
  </client>
  <runtime name="PYTHONPATH" value="${PFX}/lib/python2.7/site-packages" type="path"/>
  <use name="python"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)
