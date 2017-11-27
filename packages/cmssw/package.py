##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
from glob import glob
from string import Template
import re
import os
import fnmatch
import sys
import shutil

def relrelink(top):
    for root, dirs, files in os.walk(top,topdown=False):
       for x in files:
           p = os.path.join(root,x)
           f = os.path.abspath(p)
           if os.path.islink(f):
               linkto=os.path.realpath(f)
               if not os.path.commonprefix((f,linkto)) == '/':
                   rel=os.path.relpath(linkto,start=os.path.dirname(f))
                   os.remove(p)
                   os.symlink(rel, p)
       for y in dirs:
           p = os.path.join(root,y)
           f = os.path.abspath(p)
           if os.path.islink(f):
               linkto=os.path.realpath(f)
               if not os.path.commonprefix((f,linkto)) == '/':
                   rel=os.path.relpath(linkto,start=os.path.dirname(f))
                   os.remove(p)
                   os.symlink(rel, p)

class Cmssw(Package):
    """CMSSW built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url      = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc_amd64_gcc630/cms/cmssw/CMSSW_9_2_12/src.tar.gz"

    version('9.2.12','c66e3769785321309f70f85bc315e948')

    config_tag='V05-05-40'

    resource(name='config',
             url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/fwlite/CMSSW_9_2_13_FWLITE/%s.tar.gz'%config_tag,
             branch='master',
             placement='config'
    )
    
    resource(name='toolbox',
             git='https://github.com/gartung/scram-tool-templ.git',
             commit='97071c1',
             placement='tools'
    )


    depends_on('cmssw.scram')
    depends_on('cmssw.gmake')
    depends_on('cmssw.root@6.10.08^python+shared^fftw~mpi')
    depends_on('cmssw.tbb')
    depends_on('cmssw.tinyxml^boost+python+shared^python+shared')
    depends_on('cmssw.clhep@2.3.1.1~cxx11+cxx14')
    depends_on('cmssw.md5')
    depends_on('cmssw.python+shared')
    depends_on('cmssw.vdt')
    depends_on('cmssw.boost@1.63.0+python+shared^python+shared')
    depends_on('cmssw.libsigcpp')
    depends_on('cmssw.xrootd')
    depends_on('cmssw.cppunit')
    depends_on('cmssw.xerces-c')
    depends_on('cmssw.expat')
    depends_on('cmssw.sqlite')
    depends_on('cmssw.bzip2')
    depends_on('cmssw.gsl')
    depends_on('cmssw.hepmc')
    depends_on('cmssw.heppdt')
    depends_on('cmssw.libpng')
    depends_on('cmssw.giflib')
    depends_on('cmssw.openssl')
    depends_on('cmssw.pcre')
    depends_on('cmssw.zlib')
    depends_on('cmssw.xz')
    depends_on('cmssw.libtiff')
    depends_on('cmssw.libxml2^python+shared')
    depends_on('cmssw.bzip2')
    depends_on('cmssw.fireworks-data')
    depends_on('cmssw.cmssw.llvm@4.0.1~gold~libcxx+python+shared_libs')
    depends_on('cmssw.cfe-bindings@4.0.1')
    depends_on('cmssw.libuuid')
    depends_on('cmssw.valgrind')
    depends_on('cmssw.geant4~qt')
    depends_on('cmssw.expat')
    depends_on('cmssw.protobuf')
    depends_on('cmssw.eigen')
    depends_on('cmssw.curl')
    depends_on('cmssw.classlib')
    depends_on('cmssw.davix')
    depends_on('cmssw.gperftools')
    depends_on('cmssw.meschach')
    depends_on('cmssw.fastjet')
    depends_on('cmssw.fftjet')
    depends_on('cmssw.pythia6')
    depends_on('cmssw.pythia8')
    depends_on('cmssw.oracle')
    depends_on('cmssw.sqlite@3.16.02')
    depends_on('cmssw.coral')

    if sys.platform == 'darwin':
        patch('macos.patch')
    else:
        patch('linux.patch')

    scram_arch='linux_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch='osx10_amd64_clang'

    def install(self, spec, prefix):
        scram=which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        cmssw_version='CMSSW.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        scram_version='V'+str(spec['scram'].version)
        project_dir=join_path(prefix,cmssw_u_version)
        
        gcc=which(spack_f77)
        gcc_prefix=re.sub('/bin/.*$','',self.compiler.f77)
        gcc_machine=gcc('-dumpmachine',output=str)
        gcc_ver=gcc('-dumpversion',output=str)

        values = {}
        values['SELF_LIB']=project_dir+'/lib/'+scram_arch
        values['SELF_INC']=project_dir+'/src'
        values['GCC_VER']=gcc_ver.rstrip()
        values['GCC_PREFIX']=gcc_prefix
        values['GCC_MACHINE']=gcc_machine.rstrip()

        with working_dir(build_directory, create=True):
            rsync=which('rsync')
            mkdirp('src')
            rsync('-a', '--exclude', '.git', '--exclude', 'config',
                  '--exclude', 'spack-build.*',
                  source_directory+'/','src/')
            mkdirp('config')
            rsync('-a', '--exclude', '.git', 
                  source_directory+'/config/','config/')
            with open('config/config_tag','w') as f:
                f.write(self.config_tag)
                f.close()
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for key in spec.keys:
                xmlfiles = glob(join_path(spec[key].prefix.etc,'scram.d','*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile,'tools/selected')

            perl=which('perl')
            perl('config/updateConfig.pl',
                 '-p', 'CMSSW', 
                 '-v', cmssw_u_version,
                 '-s', scram_version,
                 '-t', build_directory,
                 '--keys', 'SCRAM_COMPILER=gcc', 
                 '--keys', 'PROJECT_GIT_HASH='+cmssw_u_version,
                 '--arch', scram_arch)
            scram('project','-d', prefix, '-b', 'config/bootsrc.xml')


        with working_dir(project_dir,create=False):
            matches = []

            for f in glob('src/*/*/test/BuildFile*'):
                matches.append(f)
            for m in matches:
                if os.path.exists(m):
                    os.remove(m)

            scram.add_default_env('LOCALTOP', project_dir)
            scram.add_default_env('CMSSW_BASE', project_dir)
            scram.add_default_env('LD_LIBRARY_PATH', project_dir+'/lib/'+scram_arch)
            scram.add_default_env('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
            scram.add_default_env('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)
            scram('build', '-v', '-k', '-j8')
            relrelink('external')
            shutil.rmtree('tmp')
#            install_tree(project_dir,prefix)


#        with working_dir(join_path(prefix,cmssw_u_version), create=False):
#            os.environ[ 'LOCALTOP' ] = os.getcwd()
#            os.environ[ 'RELEASETOP' ] = os.getcwd()
#            os.environ[ 'CMSSW_RELEASE_BASE' ] = os.getcwd()
#            os.environ[ 'CMSSW_BASE' ] = os.getcwd()
#            scram('build', 'ProjectRename')
           


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        cmssw_version='CMSSW.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        spack_env.set('LOCALTOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('RELEASETOP', self.prefix+'/'+cmssw_u_version)
        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix+'/'+cmssw_u_version+'/lib/'+scram_arch)
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)


    def setup_environment(self, spack_env, run_env):
        cmssw_version='CMSSW.'+str(self.version)
        cmssw_u_version=cmssw_version.replace('.','_')
        spack_env.set('LOCALTOP', self.prefix+'/'+cmssw_u_version)
#        spack_env.set('RELEASETOP', self.prefix+'/'+cmssw_u_version)
#        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix+'/'+cmssw_u_version+'/lib/'+scram_arch)
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        version_underscore=str(self.version).replace('.','_')
        return "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc630/cms/cmssw/CMSSW_%s/src.tar.gz" % version_underscore
