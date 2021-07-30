from spack import *
import os,sys


class Herwigpp(Package):
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
    depends_on('automake@1.15', type='build')

    patch('herwigpp-missingBoostMTLib.patch')
    patch('herwigpp-7.1.2-gcc8.patch')

    

    def install(self, spec, prefix):
        autoreconf('-fiv')
        configure('--prefix=%s'%prefix, 
                  '--enable-shared', '--disable-static',
                  '--with-thepeg=%s' % self.spec['thepeg'].prefix,
                  '--with-fastjet=%s' % self.spec['fastjet'].prefix,
                  '--with-gsl=%s' % self.spec['gsl'].prefix,
                  '--with-boost=%s' % self.spec['boost'].prefix,
                  '--with-madgraph=%s' % self.spec['madgraph5amcatnlo'].prefix,
                  '--with-gosam=%s' % self.spec['gosam'].prefix,
                  '--with-gosam-contrib=%s' % self.spec['gosamcontrib'].prefix,
                  '--with-openloops=%s' % self.spec['openloops'].prefix)
        make('all')
        make('install')
        mkdirp(prefix.bin)
        with working_dir(prefix.bin):
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
            with open('Herwig','w') as f:
                f.write(contents)
            os.chmod('Herwig',stat.S_IEXEC|stat.S_IREAD|stat.S_IWUSR|stat.S_IWGRP)
