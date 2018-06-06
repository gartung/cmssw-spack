from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Photospp(Package):
    homepage = "http://www.example.com"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/photos++/photos++-3.61-src.tgz"

    version('3.61', 'b5519bb2b22a51710f67014704f6795a')

    depends_on('hepmc')

    def install(self, spec, prefix):
        with working_dir(str(spec.version)):
            configure('--prefix=%s' % prefix, '--with-hepmc=%s' %
                      spec['hepmc'].prefix)
            make()
            make('install')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'photospp.xml'
        contents = str("""
<tool name="photospp" version="${VER}">
  <lib name="Photospp"/>
  <lib name="PhotosppHepMC"/>
  <lib name="PhotosppHEPEVT"/>
  <client>
    <environment name="PHOTOSPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PHOTOSPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$PHOTOSPP_BASE/include"/>
  </client>
  <use name="hepmc"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)
