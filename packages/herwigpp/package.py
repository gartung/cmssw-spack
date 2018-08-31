from spack import *
import os,sys


class Herwigpp(AutotoolsPackage):
    url      = "https://www.hepforge.org/archive/herwig/Herwig-7.1.4.tar.bz2"

    version('7.1.4', sha256='bdd55ac0dcc9e96d2f64fe6eaa4d7df38709e9fc3446fe16eae3200cbe0c99ab',
              url="https://www.hepforge.org/archive/herwig/Herwig-7.1.4.tar.bz2")

    depends_on('lhapdf')
    depends_on('boost')
    depends_on('thepeg')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('fastjet')
    depends_on('gosamcontrib')
    depends_on('gosam')
    depends_on('madgraph5amcatnlo')
    depends_on('openloops')

    patch('herwigpp-missingBoostMTLib.patch')
    patch('herwigpp-7.1.2-gcc8.patch')

    def configure_args(self):
        args = ['--enable-shared', '--disable-static',
                '--with-thepeg=%s' % self.spec['thepeg'].prefix,
                '--with-fastjet=%s' % self.spec['fastjet'].prefix,
                '--with-gsl=%s' % self.spec['gsl'].prefix,
                '--with-boost=%s' % self.spec['boost'].prefix,
                '--with-madgraph=%s' % self.spec['madgraph5amcatnl'].prefix,
                '--with-gosam=%s' % self.spec['gosam'].prefix,
                '--with-gosam-contrib=%s' % self.spec['gosamcontrib'].prefix,
                '--with-openloops=%s' % self.spec['openloops'].prefix ]
        return args

    def install(self, spec, prefix):
        make('all')
        make('install')
        with working_directory('prefix.bin'):
            os.rename('Herwig', 'Herwig-cms')
            contents = str("""
#!/bin/bash
REPO_OPT=""
if [ "$HERWIGPATH" != "" ] && [ -e "$HERWIGPATH/HerwigDefaults.rpo" ] ; then
  if [ $(echo " $@" | grep ' --repo' | wc -l) -eq 0 ] ; then REPO_OPT="--repo $HERWIGPATH/HerwigDefaults.rpo" ; fi
fi
$(dirname $0)/Herwig-cms $REPO_OPT "$@"
HERWIG_WRAPPER
""")
            with open('Herwig') as f:
                f.write(contents)
            os.chmod('+x','Herwig')
