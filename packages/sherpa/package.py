from spack import *
import inspect
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Sherpa(Package):
    homepage = "http://www.example.com"
    url = "http://www.hepforge.org/archive/sherpa/SHERPA-MC-2.2.2.tar.gz"

    version('2.2.2', git='https://github.com/cms-externals/sherpa', branch='cms/v2.2.2')

    depends_on('scons')
    depends_on('swig@3.0:', type='build')
    depends_on('fastjet')
    depends_on('mcfm', type='build')
    depends_on('hepmc')
    depends_on('lhapdf')
    depends_on('blackhat')
    depends_on('openloops')
    depends_on('sqlite')
    depends_on('qd')
    depends_on('boost')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')

    def install(self, spec, prefix):
        autoreconf('-i', '--force')
        self.FASTJET_ROOT=spec['fastjet'].prefix
        self.MCFM_ROOT=spec['mcfm'].prefix
        self.HEPMC_ROOT=spec['hepmc'].prefix
        self.LHAPDF_ROOT=spec['lhapdf'].prefix
        self.BLACKHAT_ROOT=spec['blackhat'].prefix
        self.OPENLOOPS_ROOT=spec['openloops'].prefix
        self.SQLITE_ROOT=spec['sqlite'].prefix
        self.OPENSSL_ROOT=spec['openssl'].prefix
        self.QD_ROOT=spec['qd'].prefix
        args = ['--prefix=%s' % prefix,
                '--enable-analysis',
                '--disable-silent-rules',
                '--enable-fastjet=%s' % self.FASTJET_ROOT,
                '--enable-mcfm=%s' % self.MCFM_ROOT,
                '--enable-hepmc2=%s' % self.HEPMC_ROOT,
                '--enable-lhapdf=%s' % self.LHAPDF_ROOT,
                '--enable-blackhat=%s' % self.BLACKHAT_ROOT,
                '--enable-pyext',
                '--enable-ufo',
                '--enable-openloops=%s' % self.OPENLOOPS_ROOT,
                '--with-sqlite3=%s' % self.SQLITE_ROOT,
                'CXX=g++', 
                'CXXFLAGS=-fuse-cxa-atexit -m64 -O2 -std=c++0x -I%s/include -I%s/include -I%s/include' %
                 (self.LHAPDF_ROOT,self.BLACKHAT_ROOT,self.OPENSSL_ROOT),
                'LDFLAGS=-ldl -L%s/lib/blackhat -L%s/lib -L%s/lib' %
                 (self.BLACKHAT_ROOT,self.QD_ROOT,self.OPENSSL_ROOT)
               ]
        configure(*args)
        make()
        make('install')

    def url_for_version(self, version):
        url = "http://www.hepforge.org/archive/sherpa/SHERPA-MC-%s.tar.gz" % str(version)
        return url

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'sherpa.xml'
        contents = str("""
<tool name="sherpa" version="${VER}">
  <lib name="SherpaMain"/>
  <lib name="ToolsMath"/>
  <lib name="ToolsOrg"/>
  <client>
    <environment name="SHERPA_BASE" default="${PFX}"/>
    <environment name="BINDIR" default="$$SHERPA_BASE/bin"/>
    <environment name="LIBDIR" default="$$SHERPA_BASE/lib/SHERPA-MC"/>
    <environment name="INCLUDE" default="$$SHERPA_BASE/include/SHERPA-MC"/>
  </client>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$SHERPA_BASE/include" type="path"/>
  <runtime name="SHERPA_SHARE_PATH" value="$$SHERPA_BASE/share/SHERPA-MC" type="path"/>
  <runtime name="SHERPA_INCLUDE_PATH" value="$$SHERPA_BASE/include/SHERPA-MC" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="PYTHONPATH" value="$$SHERPA_BASE/lib/python2.7/site-packages" type="path"/>
  <runtime name="SHERPA_LIBRARY_PATH" value="$$SHERPA_BASE/lib/SHERPA-MC" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="HepMC"/>
  <use name="lhapdf"/>
  <use name="qd"/>
  <use name="blackhat"/>
  <use name="fastjet"/>
  <use name="sqlite"/>
  <use name="openmpi"/>
  <use name="openloops"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

