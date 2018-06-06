from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FrontierClient(MakefilePackage):


    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/frontier_client/2.8.20/frontier_client__2.8.20__src.tar.gz"

    version('2.8.20', 'e2ea893b02eab539a0cf6a3812f4937c')

    patch('frontier_client-2.8.20-add-python-dbapi.patch')

    depends_on('openssl')
    depends_on('expat')
    depends_on('zlib')
    depends_on('pacparser')
    depends_on('python')

    def build(self, spec, prefix):
        make('-j1', 'EXPAT_DIR=%s' % spec['expat'].prefix,
             'PACPARSER_DIR=%s' % spec['pacparser'].prefix,
             'COMPILER_TAG=gcc_%s' % spec.compiler.version,
             'ZLIB_DIR=%s' % spec['zlib'].prefix,
             'OPENSSL_DIR=%s' % spec['openssl'].prefix,
             'CXXFLAGS=-ldl', 'CFLAGS=-I%s' % spec['openssl'].prefix.include,
             'all'
             )

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        make('-j1', 'EXPAT_DIR=%s' % spec['expat'].prefix,
             'PACPARSER_DIR=%s' % spec['pacparser'].prefix,
             'COMPILER_TAG=gcc_%s' % spec.compiler.version,
             'ZLIB_DIR=%s' % spec['zlib'].prefix,
             'OPENSSL_DIR=%s' % spec['openssl'].prefix,
             'CXXFLAGS=-ldl',
             'distdir=%s' % prefix,
             'dist'
             )
        install_tree('python', prefix + '/python')

    def url_for_version(self, version):
        """Handle version string."""
        return "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/frontier_client/%s/frontier_client__%s__src.tar.gz" % (version, version)

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'frontier_client.xml'
        contents = str("""<tool name="frontier_client" version="$VER">
  <lib name="frontier_client"/>
  <client>
    <environment name="FRONTIER_CLIENT_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$FRONTIER_CLIENT_BASE/include"/>
    <environment name="LIBDIR" default="$$FRONTIER_CLIENT_BASE/lib"/>
  </client>
  <runtime name="FRONTIER_CLIENT" value="$$FRONTIER_CLIENT_BASE/"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="openssl"/>
  <use name="expat"/>
  <runtime name="PYTHONPATH" value="$$FRONTIER_CLIENT_BASE/python/lib" type="path"/>
  <use name="python"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)
