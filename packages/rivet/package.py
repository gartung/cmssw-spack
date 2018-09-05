from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Rivet(AutotoolsPackage):
    url = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/Rivet-2.5.4.tar.bz2"

    version('3.0.0alpha1', '7fb24d0e6ac8e9fe549d61194cb863d0')
    version('2.5.4',       '709a5c744135639f8f8195a1241ae81d', preferred=True)

    depends_on('hepmc')
    depends_on('fastjet')
    depends_on('gsl')
    depends_on('yoda')
    depends_on('boost')
    depends_on('py-cython')
    depends_on('asciidoc', type='build')

    def configure_args(self):
        args = ['--disable-silent-rules',
                '--with-hepmc=%s' % self.spec['hepmc'].prefix,
                '--with-fastjet=%s' % self.spec['fastjet'].prefix,
                '--with-gsl=%s' % self.spec['gsl'].prefix,
                '--with-yoda=%s' % self.spec['yoda'].prefix,
                '--disable-doxygen',
                '--disable-pdfmanual',
                '--with-pic',
                'PYTHONPATH=%s/lib/python2.7/site-packages' % self.spec['py-cython'].prefix,
                'CPPFLAGS=-I%s' % self.spec['boost'].prefix.include
                ]
        return args

