from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Herwig(Package):
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/herwig/herwig-6.521-src.tgz"

    version('6.521.2', 'f5eebb2d2318dc437ec534eb430293d9')
    version('6.521',   '61bfc32cbf25fe92e9e3e7f23be1338f')


    depends_on('lhapdf')
    depends_on('photos')

    def install(self, spec, prefix):
        with working_dir(self.version.string):
            configure('--enable-static', '--disable-shared', '--prefix=%s' % prefix, 'F77=gfortran -fPIC')
            make('LHAPDF_ROOT=%s' % spec['lhapdf'],
                 'PHOTOS_ROOT=%s' % spec['photos'])
            make('check')
            make('install')
        os.symlink('%s/HERWIG65.INC' % prefix.include, '%s/herwig65.inc'% prefix.include)


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'herwig.xml'
        contents = str("""
<tool name="herwig" version="${VER}">
  <lib name="herwig"/>
  <lib name="herwig_dummy"/>
  <client>
    <environment name="HERWIG_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$HERWIG_BASE/lib"/>
    <environment name="INCLUDE" default="$$HERWIG_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="f77compiler"/>
  <use name="lhapdf"/>
  <use name="photos"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)
