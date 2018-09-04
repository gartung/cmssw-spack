from spack import *
import os
import distutils

class Madgraph5amcatnlo(Package):

    homepage = "https://launchpad.net/mg5amcnlo/"
    url      = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc810/external/madgraph5amcatnlo/2.6.0/MG5_aMC_v2.6.0.tar.gz"

    version('2.6.0', sha256='ba182a2d85733b3652afa87802adee60bf6a5270cc260cdb38366ada5e8afef4')

    patch('madgraph5amcatnlo-config.patch')
    patch('madgraph5amcatnlo-compile.patch')

    depends_on('python')
    depends_on('hepmc')
    depends_on('root')
    depends_on('lhapdf')
    depends_on('gosamcontrib')
    depends_on('fastjet')
    depends_on('pythia8')
    depends_on('thepeg')

    def setup_environment(self, spack_env, build_env): 
        spack_env.set('FC', spack_f77+' -std=legacy')

    def install(self, spec, prefix):
        filter_file('\${HEPMC_ROOT}', '%s'%spec['hepmc'].prefix,'input/mg5_configuration.txt')
        filter_file('\${PYTHIA8_ROOT}', '%s'%spec['pythia8'].prefix,'input/mg5_configuration.txt')
        filter_file('\${LHAPDF_ROOT}', '%s'%spec['lhapdf'].prefix,'input/mg5_configuration.txt')
        filter_file('\${FASTJET_ROOT}', '%s'%spec['fastjet'].prefix,'input/mg5_configuration.txt')
        filter_file('\${GOSAMCONTRIB_ROOT}', '%s'%spec['gosamcontrib'].prefix,'input/mg5_configuration.txt')
        filter_file('\${THEPEG_ROOT}', '%s'%spec['thepeg'].prefix,'input/mg5_configuration.txt')
        install('input/mg5_configuration.txt', 'input/mg5_configuration_patched.txt')
        python=which('python')
        python('./bin/compile.py')
        os.remove('bin/compile.py')
        os.remove('input/mg5_configuration.txt')
        install('input/mg5_configuration_patched.txt', 'input/mg5_configuration.txt')
        content=str("""
generate p p > t t~ [QCD]
output basiceventgeneration
launch
set nevents 5
""")
        with open('basiceventgeneration.txt','w') as f:
            f.write(content)
        python('./bin/mg5_aMC', 'basiceventgeneration.txt')
        for f in find('.', '*.tgz'):
            os.remove(f)
        distutils.dir_util.copy_tree('.', self.prefix)
