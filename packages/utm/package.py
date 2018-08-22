from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Utm(Package):
    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/utm/utm_0.6.7-fmblme/utm-utm_0.6.7.tgz"

    version('0.6.7', git='https://gitlab.cern.ch/cms-l1t-utm/utm.git', tag='utm_0.6.7')

    depends_on('gmake')
    depends_on('xerces-c')
    depends_on('boost')

    def patch(self):
        filter_file('CXXFLAGS = ', 'CXXFLAGS = -std=c++11 ', './tmGrammar/Makefile')
        filter_file('CXXFLAGS = ', 'CXXFLAGS = -std=c++11 ', './tmTable/Makefile')
        filter_file('CXXFLAGS = ', 'CXXFLAGS = -std=c++11 ', './tmUtil/Makefile')
        filter_file('CXXFLAGS = ', 'CXXFLAGS = -std=c++11 ', './tmXsd/Makefile')
        filter_file('CXXFLAGS = ', 'CXXFLAGS = -std=c++11 ', './tmXsd/gen-xsd-type/Makefile')


    def setup_environment(self, spack_env, run_env):
        spack_env.set('XERCES_C_BASE', '%s' % self.spec['xerces-c'].prefix)
        spack_env.set('BOOST_BASE', '%s' % self.spec['boost'].prefix)

    def install(self, spec, prefix):
        make('-f', 'Makefile.standalone', 'all')
        make('-f', 'Makefile.standalone', 'install')
        install_tree('include', prefix.include)
        install_tree('lib', prefix.lib)
        install_tree('xsd-type', prefix + '/xds-type')
        install('menu.xsd', prefix + '/menu.xsd')


