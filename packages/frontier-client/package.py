from spack import *
import sys,os

class FrontierClient(MakefilePackage):

    url = "http://frontier.cern.ch/dist/frontier_client__2.8.20__src.tar.gz"

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
        return "http://frontier.cern.ch/dist/frontier_client__%s__src.tar.gz" % version
