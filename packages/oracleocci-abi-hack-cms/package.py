from spack import *
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class OracleocciAbiHackCms(Package):
    """An ABI hack to occi.h with std=c++17"""

    homepage = "https://github.com/cms-sw"
    url = "https://github.com/cms-sw/cms_oracleocci_abi_hack.git"

    version('1.0.0', git = "https://github.com/cms-sw/cms_oracleocci_abi_hack.git", 
             commit='88b2a965305226df1822a14af8fe7174ee5f1614')

    depends_on('oracle')

    def install(self, spec, prefix):
        make()
        with working_dir('build', create=False):
            shutil.copytree('lib',prefix.lib)
            shutil.copytree('include',prefix.include)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('INCLUDE_DIR','%s' % self.spec['oracle'].prefix.include)
        spack_env.set('LIB_DIR', '%s' % self.spec['oracle'].prefix.lib)
