from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Fastjet(AutotoolsPackage):
    """."""

    homepage = "http://fastjet.fr"
    url = "http://fastjet.fr/repo/fastjet-3.1.0.tar.gz"

    version('3.3.0', git='https://github.com/cms-externals/fastjet.git', commit='20f797339b4de5eb3281b6e6c7c73bc5efd5b062')
    version('3.1.0', git='https://github.com/cms-externals/fastjet.git', commit='5e4e8ed7a6ebcca0467add9d1a22d2f7cf6cdbd3')

    def configure_args(self):
        args = [
            '--enable-shared',
            '--enable-atlascone',
            '--enable-cmsiterativecone',
            '--enable-siscone',
            '--enable-allcxxplugins'
        ]
        if 'CXXFLAGS' in env and env['CXXFLAGS']:
            env['CXXFLAGS'] += ' ' + \
                '-O3 -Wall -ffast-math -ftree-vectorize -msse3'
        else:
            env['CXXFLAGS'] = '-O3 -Wall -ffast-math -ftree-vectorize -msse3'
        return args

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'fastjet.xml'
        contents = str("""<tool name="fastjet" version="$VER">
    <info url="http://www.lpthe.jussieu.fr/~salam/fastjet/"/>
    <lib name="fastjetplugins"/>
    <lib name="fastjettools"/>
    <lib name="siscone"/>
    <lib name="siscone_spherical"/>
    <lib name="fastjet"/>
    <client>
      <environment name="FASTJET_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$FASTJET_BASE/lib"/>
      <environment name="INCLUDE" default="$$FASTJET_BASE/include"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")

        write_scram_toolfile(contents, values, fname)
