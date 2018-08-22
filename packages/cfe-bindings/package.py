from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CfeBindings(Package):

    url = "http://releases.llvm.org/5.0.0/cfe-5.0.0.src.tar.xz"

    version('5.0.0', '699c448c6d6d0edb693c87beb1cc8c6e')
    version('4.0.1', 'a6c7b3e953f8b93e252af5917df7db97')

    extends('python')

    depends_on('llvm@5.0.0~gold+python+shared_libs',
               type='build', when='@5.0.0')
    depends_on('llvm@4.0.1~gold+python+shared_libs',
               type='build', when='@4.0.1')


    def install(self, spec, prefix):
        install_tree('%s/bindings/python/clang/' %
                     self.stage.source_path,
                     self.prefix.lib + '/python2.7/site-packages/clang')
        install('%s/libclang.so' % self.spec['llvm'].prefix.lib,
                '%s/libclang.so' % self.prefix.lib)


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LLVM_BASE', self.prefix)


    @run_after('install')
    def write_scram_toolfiles(self):
        pyvers = str(self.spec['python'].version).split('.')
        pyver = pyvers[0] + '.' + pyvers[1]

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        values['LIB'] = self.spec.prefix.lib
        values['PYVER'] = pyver

        fname = 'pyclang.xml'
        contents = str("""<tool name="pyclang" version="${VER}">
  <client>
    <environment name="PYCLANG_BASE" default="${PFX}"/>
  </client>
  <runtime name="PYTHONPATH" value="${LIB}/python${PYVER}/site-packages" type="path"/>
  <use name="python"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, self.spec.prefix)
