from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CfeBindings(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('llvm@6.0.1~gold+python+shared_libs',
               type='build')
    extends('python')

    def install(self, spec, prefix):
        install_tree( '%s/python2.7/site-packages/clang' %
                       spec['llvm'].prefix.lib,
                      '%s/python2.7/site-packages/clang' %
                     self.prefix.lib)
        install('%s/libclang.dylib' % self.spec['llvm'].prefix.lib,
                '%s/libclang.dylib' % self.prefix.lib)


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
    <environment name="LLVM_BASE" default="${PFX}"/>
    <environment name="PYCLANG_BASE" default="${PFX}"/>
  </client>
  <runtime name="PYTHONPATH" value="${LIB}/python${PYVER}/site-packages" type="path"/>
  <use name="python"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, self.spec.prefix)
